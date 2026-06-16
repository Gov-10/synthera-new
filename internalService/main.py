from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import  History, sessionLocal
from redis import Redis
import os, json, jwt, boto3
from dotenv import load_dotenv
from utils.extractor import extract, extract_ocr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from utils.vec_help import build_vector_store
load_dotenv()
app = FastAPI()
redis_client=Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), password=os.getenv("REDIS_PASSWORD"), decode_responses=False)
s3= boto3.client('s3', region_name=os.getenv("S3_REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
bucket=os.getenv("S3_BUCKET_NAME")
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

class SumSchema(BaseModel):
    job_id: str

class AskSchema(BaseModel):
    job_id: str
    question: str
llm = ChatGroq(model="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY"))


@app.get("/")
def chek():
    return {"status": "Running"}

@app.post("/summarize")
def summar(payload: SumSchema, request: Request, db:Session=Depends(get_db)):
    token=request.headers["Authorization"]
    if not token:
        raise HTTPException(status_code=401, detail="no token found")
    schema, token=token.split()
    if schema.lower() != "bearer":
        raise HTTPException(status_code=401, detail="invalid token format")
    pay = jwt.decode(token, "supersecret", algorithms=["HS256"])
    username=pay["sub"]
    job_id=payload.job_id
    key=f"job:{job_id}"
    dt=redis_client.get(key)
    if not dt:
        raise HTTPException(status_code=404, detail="no data found, please upload again")
    data=json.loads(dt)
    if data["username"] != username:
        raise HTTPException(status_code=401, detail="nah broski, this file ain't yours")
    file_key=data["file_key"]
    resp=s3.get_object(Bucket=bucket, Key=file_key)
    file_bytes=resp["Body"].read()
    text=extract(file_bytes)
    if len(text.strip()) < 100:
        text=extract_ocr(file_bytes)
    vector_store = build_vector_store(text,job_id)
    prompt = ChatPromptTemplate.from_template(
    """
    Create a professional executive summary.
    Include:
    - Main purpose
    - Key findings
    - Risks
    - Action items
    - Important conclusions
    DOCUMENT:
    {text}
    """
)
    chain = prompt | llm
    summary = chain.invoke({ "text": text[:15000]})
    summary_text = summary.content
    his=db.query(History).filter(History.job_id==job_id, History.user==username).first()
    if not his:
        raise HTTPException(status_code=404, detail="no related history found")
    his.content=summary_text
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    return {"job_id": job_id,"summary": summary_text}

@app.post("/ask")
def ask_ai(payload: AskSchema, request: Request):
    token=request.headers["Authorization"]
    if not token:
        raise HTTPException(status_code=401, detail="no token found")
    schema, token=token.split()
    if schema.lower() != "bearer":
        raise HTTPException(status_code=401, detail="invalid token format")
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    username=pay["sub"]
    embedding_model = HuggingFaceEmbeddings( model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(f"vector_indexes/{payload.job_id}",embedding_model,allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(payload.question)
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )
    qa_prompt = ChatPromptTemplate.from_template(
        """
        Answer ONLY using the context.
        If answer does not exist
        say:
        "Not found in document."
        CONTEXT:
        {context}

        QUESTION:
        {question}
        """
    )
    chain = qa_prompt | llm
    response = chain.invoke({"context": context,"question": payload.question})
    return {"question": payload.question,"answer": response.content}











