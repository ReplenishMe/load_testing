import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import fetch_one

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestShoppingList(FastHttpUser):
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
    def create_shopping_list(self):
        vendor = fetch_one('vendor')
        product = fetch_one('product')
        location = fetch_one('location')
        bin = fetch_one('bin')
        payload = {
                "bin_id": bin['id'],
                "quantity": 50,
                "product_id": product['id'],
                "location_id": location['id'],
                "vendor_id": vendor['id']
            }
        self.client.post(
            url=f"/api/{self._slug}/shopping_list",
            headers=self.default_headers,
            json=payload
        )
   
    @task(1)
    def get_shopping_list(self):
        self.client.get(
            url=f"/api/{self._slug}/shopping_list?page=1",
            headers=self.default_headers
        )

    @task(1)
    def get_shopping_list_id(self):
        shopping_list = fetch_one('shopping_list')
        self.client.get(
            url=f"/api/{self._slug}/shopping_list/{shopping_list['id']}",
            headers=self.default_headers
        )
    
    @task(1)
    def delete_shopping_list_id(self):
        shopping_list = fetch_one('shopping_list')
        self.client.delete(
            url=f"/api/{self._slug}/shopping_list?ids={shopping_list['id']}",
            headers=self.default_headers
        )

    @task(1)
    def delete_shopping_list(self):
        shopping_list = fetch_one('shopping_list')
        payload = {"ids": shopping_list['id']}
        self.client.delete(
            url=f"/api/{self._slug}/shopping_list",
            headers=self.default_headers,
            json=payload
        )

    @task(1)                                      
    def update_shopping_list_id(self):
        shopping_list = fetch_one('shopping_list')
        vendor = fetch_one('vendor')
        product = fetch_one('product')
        location = fetch_one('location')
        payload = {
                "bin_id": bin['id'],
                "quantity": 50,
                "product_id": product['id'],
                "location_id": location['id'],
                "vendor_id": vendor['id']
            }
        self.client.put(
            url=f"/api/{self._slug}/shopping_list/{shopping_list['id']}",
            headers=self.default_headers,
            json=payload
        )

