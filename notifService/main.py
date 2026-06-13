from fastapi import FastAPI, HTTPException, Request, status, Response
import os, json, boto3, logging, json
from dotenv import load_dotenv
from utils.em_send import email_send
from fastapi.responses import JSONResponse
from metric import NOTIF_SENT
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (OTLPSpanExporter)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
load_dotenv()
app= FastAPI()
s3= boto3.client('s3', region_name=os.getenv("S3_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("notif")
bucket_name=os.getenv("S3_BUCKET_NAME")
resource = Resource.create({"service.name": "notif-service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
otlp_exporter = OTLPSpanExporter( endpoint="jaeger.tracing.svc.cluster.local:4317",insecure=True,)
provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)
FastAPIInstrumentor.instrument_app(app)
tracer = trace.get_tracer(__name__)
@app.on_event("startup")
def startup():
    logger.info(json.dumps({"event": "notif_service_start", "pod": os.getenv("HOSTNAME")}))

@app.get("/")
def chek():
    return {"status": "Running"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/notify")
async def notif(request: Request):
    try:
        body = await request.json()
        email, file_key=body.get("email"), body.get("file_key")
        logger.info(json.dumps({"event":"req_receieved"}))
        pres=s3.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': bucket_name, "Key": file_key})
        email_send(email, pres)
        logger.info(json.dumps({"event": "email_sent", "email": email, "pres": pres}))
        NOTIF_SENT.inc()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "email sent"})
    except Exception as e:
        logger.error(json.dumps({"event": "notif_service_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="error getting request")

        





