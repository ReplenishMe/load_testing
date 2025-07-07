import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    fetch_one, 
    generate_text
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestBin(FastHttpUser):
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
    def create_bin(self):
        name = generate_text()
        bin_family = fetch_one('bin_family')
        payload = {"name": name, "bin_family_id": bin_family['id']}
        with self.client.post(
            url="/api/jared/bins",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("bin created successfully")
                resp.success()
            else:
                logger.error(f"Failed to create bin: {resp.status_code}")
                resp.failure("Failed to create bin")
  
    @task(1)
    def get_bin(self):
        with self.client.get(
            url="api/jared/bins",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("bin fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch bin: {resp.status_code}")
                resp.failure("Failed to fetch bin")
    
    @task(1)                         
    def update_bin_id(self):
        bin = fetch_one('bin')
        name = generate_text()
        payload = {"name": name}
        with self.client.put(
            url=f"/api/jared/bins/{bin['id']}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"bin {bin['id']} updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update bin {bin['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update bin by ID")
    
    @task(1)
    def get_bin_id(self):
        bin = fetch_one('bin')
        with self.client.get(
            url=f"/api/jared/bins/{bin['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"bin {bin['id']} fetched successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch bin {bin['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to fetch bin by ID")

    @task(1)
    def delete_bin_id(self):
        bin = fetch_one('bin')
        with self.client.delete(
            url=f"/api/jared/bins/{bin['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"bin {bin['id']} deleted successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to delete bin {bin['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to delete bin by ID")