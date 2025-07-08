import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    fetch_one,
    generate_text,
    generate_digit
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestProduct(FastHttpUser):
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
    def create_products(self):
        payload = {
                    "part_number": generate_digit(),
                    "name": generate_text(),
                    "description": generate_text(),
                    "preferred_vendor_id": 1,
                    "preferred_vendor_part_number": generate_digit(),
                    "erp_part_number": generate_digit(),
                    "uom": "0",
                    "is_external": True,
                    "active": True
                    }    
        self.client.post(
            url=f"/api/{self._slug}/products",
            headers=self.default_headers,
            json=payload
        )
    
    @task(1)
    def get_products(self):
        self.client.get(
            url=f"/api/{self._slug}/products",
            headers=self.default_headers
        )

    @task(1)
    def get_product_by_id(self):
        product = fetch_one('product')
        self.client.get(
            url=f"/api/{self._slug}/products/{product['id']}",
            headers=self.default_headers
        )          
  
    @task(1)               
    def update_product_id(self):
        product = fetch_one('product')
        name = generate_text()
        payload = {
                   "description": name,
                   "erp_part_number": "",
                   "name": name,
                   "part_number": name,
                }
        self.client.put(
            url=f"/api/{self._slug}/products/{product['id']}",
            headers=self.default_headers,
            json=payload
        )
    
    # @task(1)
    # def delete_product_id(self):
    #     product = fetch_one_asc('product')
    #     self.client.delete(
    #         url=f"/api/{self._slug}/products/{product['id']}",
    #         headers=self.default_headers
    #     )
    
    @task(1)
    def get_product_by_partnumber(self):
        self.client.get(
            url=f"/api/{self._slug}/products/partnumbers",
            headers=self.default_headers
        )

    @task(1)
    def get_product_lookup(self):
        product = fetch_one('product')
        self.client.get(
            url=f"/api/{self._slug}/products/lookup/?part_number={
                                            product['part_number']}",
            headers=self.default_headers
        )

    # @task(1)
    # def get_product_by_name(self):
    #     product = fetch_all('product')
    #     self.client.get(
    #         url=f"/api/{self._slug}/products/{product['name']}",
    #         headers=self.default_headers
    #     )
    
    @task(1)
    def get_products_report(self):
        product = fetch_one('product')
        self.client.get(
            url=f"/api/{self._slug}/products/{product['id']}/report",
            headers=self.default_headers
        )