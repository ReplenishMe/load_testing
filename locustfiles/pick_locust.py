import os
import random
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestPick(FastHttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        payload = {
            "email": os.getenv("email"),
            "password": os.getenv("password")
            }
        response = self.client.post(
            url="/auth/default/system/login",
            headers={"Accept-Encoding": "gzip, deflate, br"},
            data=payload
            )
        response.raise_for_status()
        token = response.json()['data']['access_token']

        self.default_headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Encoding": "gzip, deflate, br",
            }
        self._slug = os.getenv('ORG_SLUG')
    
    @task(1)                                   
    def create_pick(self):
        docid_str = os.getenv("docid")
        docid = docid_str.split(",") 
        docid = random.choice(docid)
        payload = {
                "docid": docid,
                "pick_type": "new",
                }
        self.client.post(
            url=f"/api/{self._slug}/pick",
            headers=self.default_headers,
            json=payload
        )
  
    @task(1)
    def get_pick(self):
        self.client.get(
            url=f"/api/{self._slug}/pick",
            headers=self.default_headers
        )
    
    @task(1)                                      
    def update_pick_id(self):
        docid_str = os.getenv("docid")
        docid = docid_str.split(",")  
        docid = random.choice(docid)
        pick_str = os.getenv("pick_id")
        pick = pick_str.split(",") 
        pick = random.choice(pick)
        payload = {
                "docid": docid,
                "pick_type": "new",
                }
        self.client.put(
            url=f"/api/{self._slug}/pick/{pick}",
            headers=self.default_headers,
            json=payload
        )
    
    @task(1)
    def get_pick_id(self):
        pick_str = os.getenv("pick_id")
        pick = pick_str.split(",")  
        pick = random.choice(pick)
        self.client.get(
            url=f"/api/{self._slug}/pick/{pick}",
            headers=self.default_headers
        )
    
    @task(1)
    def delete_pick_id(self):
        pick_str = os.getenv("pick_id")
        pick = pick_str.split(",")  
        pick = random.choice(pick)
        self.client.delete(
            url=f"/api/{self._slug}/pick/{pick}",
            headers=self.default_headers
        )