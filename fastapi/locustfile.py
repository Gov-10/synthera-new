from locust import HttpUser, task, between
import os
from dotenv import load_dotenv
load_dotenv()
class SyntheraUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = os.getenv("TEST_ID_TOKEN")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    @task(3)
    def cached_query(self):
        self.client.post(
            "/agent-run",
            json={"user_input": "What is pneumonia"},
            headers=self.headers
        )

    @task(1) 
    def uncached_query(self):
        self.client.post(
            "/agent-run",
            json={"user_input": "What is the scope of rare pulmonary fibrosis in India?"},
            headers=self.headers
        )
