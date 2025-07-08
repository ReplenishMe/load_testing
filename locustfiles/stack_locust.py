import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    fetch_one,
    fetch_one_stack,
    fetch_stack_lp
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestStack(FastHttpUser):
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
    def get_stack(self):
        self.client.get(
            url=f"/api/{self._slug}/stack",
            headers=self.default_headers
        )
    
    @task(1)
    def stack_start(self):
        loc = fetch_one('location')
        production_order = fetch_one('production_order')
        payload = {
                "location_id": loc['id'],
                "production_order_id": production_order['docid']
                }
        self.client.post(
            url=f"/api/{self._slug}/stack/start",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def close_stack(self):
        stack = fetch_one_stack('stack')
        stack_lp = fetch_stack_lp(
            'licenseplates', stack["product_id"], stack["location_id"]
        )
        payload = {
            "item_count": 0,
            "qrs": [stack_lp],
            "stack_id": stack['id']
            }
        self.client.post(
            url=f"/api/{self._slug}/stack/close",
            headers=self.default_headers,
            json=payload
        )


                     
    
