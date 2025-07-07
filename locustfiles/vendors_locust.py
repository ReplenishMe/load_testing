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
    def create_vendor(self):
        erp = generate_digit(3)
        name = generate_text()
        payload = {
                    "name": name,
                    "erp_number": erp
                }
        with self.client.post(
            url="/api/jared/vendors",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("vendors created successfully")
                resp.success()
            else:
                logger.error(f"Failed to create vendors: {resp.status_code}")
                resp.failure("Failed to create vendors")
    
    @task(1)
    def get_vendor(self):
        with self.client.get(
            url="/api/jared/vendors",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("vendors fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch vendors: {resp.status_code}")
                resp.failure("Failed to fetch vendors")
    
    @task(1)                                      
    def update_vendor_id(self):
        vendors = fetch_one('vendor')
        name = generate_text(5)
        erp = generate_text(5)
        payload = {
                "name": name,
                "erp_number":  erp,
            }
        with self.client.put(
            url=f"/api/jared/vendors/{vendors['id']}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            
            if resp.status_code == 200:
                logger.info(
                    f"vendor {vendors['id']} updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update vendor {vendors['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update vendor by id")

    @task(1)
    def get_vendor_id(self):
        vendors = fetch_one('vendor')
        with self.client.get(
            url=f"/api/jared/vendors/{vendors['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"vendor id {vendors['id']} fetched successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch vendor id {vendors['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to fetch vendors by id")
    
    @task(1)
    def delete_vendor_id(self):
        vendors = fetch_one_asc('vendor')
        with self.client.delete(
            url=f"/api/jared/vendors/{vendors['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"vendors {vendors['id']} deleted successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to delete vendors {vendors['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to delete vendors by id")
    
    