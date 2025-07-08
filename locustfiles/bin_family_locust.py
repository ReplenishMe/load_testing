import os
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import fetch_one

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestBinFamily(FastHttpUser):
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
    def create_bin_family(self):
        product = fetch_one('product')
        location = fetch_one('location')
        payload = {
                "default_quantity": 123,
                "location_id": location['id'],
                "preferred_vendor_id": product['preferred_vendor_id'],
                "product_id": product['id']
                }
        self.client.post(
            url=f"/api/{self._slug}/bin_families",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def get_bin_family(self):
        self.client.get(
            url=f"/api/{self._slug}/bin_families",
            headers=self.default_headers
        )
    
    @task(1)                                      
    def update_bin_family_id(self):
        bin_family = fetch_one('bin_family')
        product = fetch_one('product')
        location = fetch_one('location')
        payload = {
                "default_quantity": 123,
                "location_id": location['id'],
                "preferred_vendor_id": bin_family['preferred_vendor_id'],
                "product_id": product['id']
                }
        self.client.put(
            url=f"/api/{self._slug}/bin_families/{bin_family['id']}",
            headers=self.default_headers,
            json=payload
        )
    
    @task(1)
    def get_bin_family_id(self):
        bin_family = fetch_one('bin_family')
        self.client.get(
            url=f"/api/{self._slug}/bin_families/{bin_family['id']}",
            headers=self.default_headers
        )
    
    @task(1)
    def delete_bin_family_id(self):
        bin_family = fetch_one('bin_family')
        self.client.delete(
            url=f"/api/{self._slug}/bin_families/{bin_family['id']}",
            headers=self.default_headers
        )