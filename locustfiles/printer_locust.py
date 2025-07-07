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
        try:
            response = requests.post(
                url="http://localhost:5000/auth/default/system/login",
                data=payload,
                )
            response.raise_for_status()
            token = response.json()['data']['access_token']
        except Exception as e:
            logger.error(e)

        self.default_headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Encoding": "gzip, deflate, br",
            }
    
    @task(1)                                   
    def create_printers(self):
        name = generate_text(5)
        payload = {
                "name": name,
                "url": "new@gmail.com"
                }
        with self.client.post(
            url="/api/jared/printers",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("printers created successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to create printers: {resp.status_code}"
                    )
                resp.failure("Failed to create printers")
  
    @task(1)
    def get_printers(self):
        with self.client.get(
            url="api/jared/printers",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("printers fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch printers: {resp.status_code}")
                resp.failure("Failed to fetch printers")
    
    @task(1)                                      
    def update_printers_id(self):
        name = generate_text(5)
        printer_id_str = os.getenv("printer_id")
        printer_id = printer_id_str.split(",")  # now it's a list
        printer_id = random.choice(printer_id)
        payload = {
                "name": name,
                "url": "new@gmail.com"
                }
        with self.client.put(
            url=f"/api/jared/printers/{printer_id}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"printers {printer_id} updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update printers {printer_id}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update printers by ID")
    
    @task(1)
    def get_printers_id(self):
        printer_id_str = os.getenv("printer_id")
        printer_id = printer_id_str.split(",")  # now it's a list
        printer_id = random.choice(printer_id)
        with self.client.get(
            url=f"/api/jared/printers/{printer_id}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"printers {printer_id} fetched successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch printers {printer_id}: {
                        resp.status_code
                        }"
                )
                resp.failure("Failed to fetch printers by ID")
    
    @task(1)
    def delete_printers_id(self):
        printer_id_str = os.getenv("printer_id")
        printer_id = printer_id_str.split(",")  # now it's a list
        printer_id = random.choice(printer_id)
        with self.client.delete(
            url=f"/api/jared/printers/{printer_id}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"printers {printer_id} deleted successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to delete printers {printer_id}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to delete printers by id")