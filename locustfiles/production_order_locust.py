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


class LoadTestProductionOrder(FastHttpUser):
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
    def create_production_orders(self):
        product = fetch_one('product')
        external_docid = generate_text(5)
        digit_qty = generate_digit(4)
        payload = {
                    "external_docid": external_docid,
                    "product_id": product['id'],
                    "requested_qty": digit_qty
                    }
        self.client.post(
            url=f"/api/{self._slug}/production_orders",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def get_production_orders(self):
        self.client.get(
            url=f"/api/{self._slug}/production_orders",
            headers=self.default_headers
        )
             
    @task(1)
    def get_production_orders_id(self):
        production_order = fetch_one('production_order')
        self.client.get(
            url=f"/api/{self._slug}/production_orders/{production_order['id']}",
            headers=self.default_headers
        )

    @task(1)
    def patch_production_orders_id(self):
        requested_qty = generate_digit(5)
        production_order = fetch_one('production_order')
        payload = {
                    "requested_qty": requested_qty,
                }
        self.client.patch(
            url=f"/api/{self._slug}/production_orders/{production_order['id']}",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def patch_production_orders_id_permissions(self):
        production_order = fetch_one('production_order')
        payload = {
                    "add": [2],
                    "remove": [4, 8, 16, 64, 32, 128]
                }
        self.client.patch(
            url=f'''/api/{self._slug}/production_orders/{
                production_order['id']
                }/public_view_permissions''',
            headers=self.default_headers,
            json=payload
        ) 
  
    @task(1)
    def production_orders_email_report(self):
        payload = {"email": "shyamgundetin@gmail.com"}
        self.client.post(
            url=f"/api/{self._slug}/production_orders/email_report",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def productionorder_status_report(self):
        production_order = fetch_one('production_order')
        self.client.get(
            url=f"""/api/{self._slug}/production_orders/{
                production_order['id']
                }/status_report?page=1""",
            headers=self.default_headers
        )

    @task(1)
    def get_production_order_lookup(self):
        production_order = fetch_one('production_order')
        self.client.get(
            url=f"/api/{self._slug}/production_orders/lookup?docid={
                production_order['docid']
                }",
            headers=self.default_headers
        )
              
    @task(1)
    def get_production_orders_page(self):
        self.client.get(
            url=f"/api/{self._slug}/production_orders?page=1&per_page=50",
            headers=self.default_headers
        )

    @task(1)
    def get_production_orders_keyword(self):
        production_order = fetch_one('production_order')
        self.client.get(
            url=f'''/api/{self._slug}/production_orders?keyword={
                production_order['external_docid']
                }&page=1&per_page=50''',
            headers=self.default_headers
        )