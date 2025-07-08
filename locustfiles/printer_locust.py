import os
import random
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import generate_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestPrinters(FastHttpUser):
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
    def create_printers(self):
        name = generate_text(5)
        payload = {
                "name": name,
                "url": "new@gmail.com"
                }
        self.client.post(
            url=f"/api/{self._slug}/printers",
            headers=self.default_headers,
            json=payload
        )
  
    @task(1)
    def get_printers(self):
        self.client.get(
            url=f"/api/{self._slug}/printers",
            headers=self.default_headers
        )
    
    @task(1)                                      
    def update_printers_id(self):
        name = generate_text(5)
        printer_id_str = os.getenv("printer_id")
        printer_id = printer_id_str.split(",")
        printer_id = random.choice(printer_id)
        payload = {
                "name": name,
                "url": "new@gmail.com"
                }
        self.client.put(
            url=f"/api/{self._slug}/printers/{printer_id}",
            headers=self.default_headers,
            json=payload
        )
    
    @task(1)
    def get_printers_id(self):
        printer_id_str = os.getenv("printer_id")
        printer_id = printer_id_str.split(",")
        printer_id = random.choice(printer_id)
        self.client.get(
            url=f"/api/{self._slug}/printers/{printer_id}",
            headers=self.default_headers
        )
    
    @task(1)
    def delete_printers_id(self):
        printer_id_str = os.getenv("printer_id")
        printer_id = printer_id_str.split(",")
        printer_id = random.choice(printer_id)
        self.client.delete(
            url=f"/api/{self._slug}/printers/{printer_id}",
            headers=self.default_headers
        )