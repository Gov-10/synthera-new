from kafka import KafkaConsumer
import os, json
from dotenv import load_dotenv
load_dotenv()
from redis import Redis
redis_client=Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), password=os.getenv("REDIS_PASSWORD"), decode_responses=True)
from langchain_groq import ChatGroq
llm = ChatGroq(model="", api_key=os.getenv("GROQ_API_KEY"))
BOOTSTRAP_SERVER=""
consumer=KafkaConsumer("iqvia-worker", "patent-worker", "web-worker", "exim-worker", bootstrap_servers=BOOTSTRAP_SERVER, value_deserializer=lambda x: json.loads(x.decode()), group_id="report-group")
store = {}
REQUIRED = {
    "iqvia",
    "patent",
    "web",
    "exim"
}
for msg in consumer:
    event = msg.value
    topic = msg.topic
    job_id=event["job_id"]
    if job_id not in store:
        store[job_id] = {}
    if topic == "iqvia-worker":
        store[job_id]["iqvia"] = event["iqvia_res"]
    if topic == "patent-worker":
        store[job_id]["patent"] = event["patent_res"]
    if topic == "web-worker":
        store[job_id]["web"] = event["web_res"]
    if topic=="exim-worker":
        store[job_id]["exim"] = event["exim_res"]
    report= store[job_id]
    if REQUIRED.issubset(report.keys()):
        try:
            tmp_dir = ensure_tmp_dir()
            chart_paths = []
            if report.get("iqvia"):
                chart_paths.extend(
                    make_iqvia_charts(
                        report["iqvia"],
                        tmp_dir
                    )
                )
            if report.get("exim"):
                chart_paths.extend(
                    make_exim_charts(
                        report["exim"],
                        tmp_dir
                    )
                )
            if report.get("patent"):
                chart_paths.extend(
                    make_patent_charts(
                        report["patent"],
                        tmp_dir
                    )
                )
            report_parts = []
            report_parts.append("# Intelligence Report")
            if report.get("iqvia"):
                report_parts.append("\n## IQVIA Market Insights")
                report_parts.append(
                    json.dumps(
                        report["iqvia"],
                        indent=2
                    )
                )
            if report.get("exim"):
                report_parts.append("\n## EXIM Trade Insights")
                report_parts.append(
                    json.dumps(
                        report["exim"],
                        indent=2
                    )
                )
            if report.get("patent"):
                report_parts.append("\n## Patent Landscape")
                report_parts.append(
                    json.dumps(
                        report["patent"],
                        indent=2
                    )
                )
            if report.get("web"):
                report_parts.append("\n## Web Intelligence")
                report_parts.append(
                    str(report["web"])
                )
            report_text = "\n".join(report_parts)
            pdf_local_path = os.path.join(
                tmp_dir,
                f"report_{uuid.uuid4().hex}.pdf"
            )
            build_pdf(
                report_text,
                chart_paths,
                pdf_local_path
            )
            file_key = (
                f"reports/{uuid.uuid4().hex}.pdf"
            )
            s3.upload_file(
                Filename=pdf_local_path,
                Bucket=S3_BUCKET_NAME,
                Key=file_key,
                ExtraArgs={
                    "ContentType":
                    "application/pdf"
                }
            )
            pdf_url = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": S3_BUCKET_NAME,
                    "Key": file_key
                },
                ExpiresIn=3600
            )
            redis_client.hset(
                f"job:{job_id}",
                mapping={
                    "status": "COMPLETED",
                    "pdf_url": pdf_url,
                    "pdf_s3_key": file_key,
                    "report": report_text
                }
            )
            del store[job_id]
        except Exception as e:
            redis_client.hset(
                f"job:{job_id}",
                mapping={
                    "status": "FAILED",
                    "error": str(e)
                }
                )

#TODO: add util functions...kya matlab fatigue does not mean I am allowed to copy paste AI ka code (sed emoji)
