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
for msg in consumer:
    event = msg.value
    topic = msg.topic
    job_id=event["job_id"]
    if job_id not in store:
        store[job_id] = {}
    if topic == "iqvia-worker":
        store[job_id]["iqvia"] = data["iqvia_res"]
    if topic == "patent-worker":
        store[job_id]["patent"] = data["patent_res"]
    if topic == "web-worker":
        store[job_id]["web"] = data["web_res"]
    if topic=="exim-worker":
        store[job_id]["exim"] = data["exim_res"]
    report= store[job_id]
    if ("iqvia" in report and "patent" in report and "web" in report and "exim" in report):
        pass

    
