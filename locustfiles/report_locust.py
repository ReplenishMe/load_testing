import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, constant
from locust.contrib.fasthttp import FastHttpUser
from db import fetch_one

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestReport(FastHttpUser):
    wait_time = constant(5)

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
    def order_report(self):
        production_order = fetch_one('production_order')
        payload = {
                    "order_id": production_order['id'],
                    "email": "shyamgundetin@gmail.com"
                }
        self.client.post(
            url=f"/api/{self._slug}/reports/orders",
            headers=self.default_headers,
            json=payload
        )
     
    @task(1)                                      
    def everything_report(self):
        payload = {  
                    "email": "shyamgundetin@gmail.com"
                }
        self.client.post(
            url=f"/api/{self._slug}/reports/everything_report",
            headers=self.default_headers,
            json=payload
        )

    