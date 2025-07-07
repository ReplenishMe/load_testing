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


class LoadTestBinFamily(FastHttpUser):
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
    def create_bin_family(self):
        product = fetch_one('product')
        location = fetch_one('location')
        payload = {
                "default_quantity": 123,
                "location_id": location['id'],
                "preferred_vendor_id": product['preferred_vendor_id'],
                "product_id": product['id']
                }
        with self.client.post(
            url="/api/jared/bin_families",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("bin_family created successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to create bin_family: {resp.status_code}"
                    )
                resp.failure("Failed to create bin_family")
  
    @task(1)
    def get_bin_family(self):
        with self.client.get(
            url="api/jared/bin_families",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("bin_family fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch bin_family: {resp.status_code}")
                resp.failure("Failed to fetch bin_family")
    
    @task(1)                                      
    def update_bin_family_id(self):
        bin_family = fetch_one('bin_family')
        payload = {
                "default_quantity": 123,
                "location_id": bin_family['id'],
                "preferred_vendor_id": bin_family['preferred_vendor_id'],
                "product_id": bin_family['id']
                }
        with self.client.put(
            url=f"/api/jared/bin_families/{bin_family['id']}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"bin_family [{bin_family['id']}] updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update bin_family [{bin_family['id']}]: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update bin_family by ID")
    
    @task(1)
    def get_bin_family_id(self):
        bin_family = fetch_one('bin_family')
        with self.client.get(
            url=f"/api/jared/bin_families/{bin_family['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"bin_family [{bin_family['id']}] fetched successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch bin_family [{bin_family['id']}]: {
                        resp.status_code
                        }"
                )
                resp.failure("Failed to fetch bin_family by ID")
    
    @task(1)
    def delete_bin_family_id(self):
        bin_family = fetch_one('bin_family')
        with self.client.delete(
            url=f"/api/jared/bin_families/{bin_family['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"bin_family [{bin_family['id']}] deleted successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to delete bin_family [{bin_family['id']}]: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to delete bin_family by ID")