import os
from celery import Celery 
from dotenv import load_dotenv
load_dotenv()
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
celery = Celery("synthera_tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND, include=["tasks.notification_tasks"])
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)