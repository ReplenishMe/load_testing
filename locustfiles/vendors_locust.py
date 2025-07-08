import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    fetch_one,
    generate_digit,
    generate_text,
    fetch_one_asc
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestVendors(FastHttpUser):
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
    def create_vendor(self):
        erp = generate_digit(3)
        name = generate_text()
        payload = {
                    "name": name,
                    "erp_number": erp
                }
        self.client.post(
            url=f"/api/{self._slug}/vendors",
            headers=self.default_headers,
            json=payload
        )
    
    @task(1)
    def get_vendor(self):
        self.client.get(
            url=f"/api/{self._slug}/vendors",
            headers=self.default_headers
        )
    
    @task(1)                                      
    def update_vendor_id(self):
        vendors = fetch_one('vendor')
        name = generate_text(5)
        erp = generate_text(5)
        payload = {
                "name": name,
                "erp_number":  erp,
            }
        self.client.put(
            url=f"/api/{self._slug}/vendors/{vendors['id']}",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def get_vendor_id(self):
        vendors = fetch_one('vendor')
        self.client.get(
            url=f"/api/{self._slug}/vendors/{vendors['id']}",
            headers=self.default_headers
        )
    
    @task(1)
    def delete_vendor_id(self):
        vendors = fetch_one_asc('vendor')
        self.client.delete(
            url=f"/api/{self._slug}/vendors/{vendors['id']}",
            headers=self.default_headers
        )
    
