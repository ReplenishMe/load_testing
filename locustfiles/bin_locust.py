import os
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    fetch_one, 
    generate_text
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestBin(FastHttpUser):
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
    def create_bin(self):
        name = generate_text()
        bin_family = fetch_one('bin_family')
        payload = {"name": name, "bin_family_id": bin_family['id']}
        self.client.post(
            url=f"/api/{self._slug}/bins",
            headers=self.default_headers,
            json=payload
        )
  
    @task(1)
    def get_bin(self):
        self.client.get(
            url=f"/api/{self._slug}/bins",
            headers=self.default_headers
        )
    
    @task(1)                         
    def update_bin_id(self):
        bin = fetch_one('bin')
        name = generate_text()
        payload = {"name": name}
        self.client.put(
            url=f"/api/{self._slug}/bins/{bin['id']}",
            headers=self.default_headers,
            json=payload
        )
    
    @task(1)
    def get_bin_id(self):
        bin = fetch_one('bin')
        self.client.get(
            url=f"/api/{self._slug}/bins/{bin['id']}",
            headers=self.default_headers
        )

    @task(1)
    def delete_bin_id(self):
        bin = fetch_one('bin')
        self.client.delete(
            url=f"/api/{self._slug}/bins/{bin['id']}",
            headers=self.default_headers
        )