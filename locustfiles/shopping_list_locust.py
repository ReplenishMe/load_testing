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
        with self.client.post(
            url="/api/jared/shopping_list",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("shopping_list created successfully")
                resp.success()
            else:
                logger.error(f'''Failed to create shopping_list: {
                    resp.status_code
                    }''')
                resp.failure("Failed to create shopping_list")
   
    @task(1)
    def get_shopping_list(self):
        with self.client.get(
            url="/api/jared/shopping_list?page=1",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            import time
            time.sleep(2)
            if resp.status_code == 200:
                logger.info("shopping_list fetched successfully")
                resp.success()
            else:
                logger.error(f'''Failed to fetch shopping_list: {
                    resp.status_code
                    }''')
                resp.failure("Failed to fetch shopping_list")

    @task(1)
    def get_shopping_list_id(self):
        shopping_list = fetch_one('shopping_list')
        with self.client.get(
            url=f"/api/jared/shopping_list/{shopping_list['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"shopping_list {shopping_list['id']} fetched successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch shopping_list {shopping_list['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to fetch bin by ID")
    
    @task(1)
    def delete_shopping_list_id(self):
        shopping_list = fetch_one('shopping_list')
        with self.client.delete(
            url=f"/api/jared/shopping_list?ids={shopping_list['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"shopping_list {shopping_list['id']} deleted successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to delete shopping_list {shopping_list['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to delete shopping_list by ID")

    @task(1)
    def delete_shopping_list(self):
        shopping_list = fetch_one('shopping_list')
        payload = {"ids": shopping_list['id']}
        with self.client.delete(
            url="/api/jared/shopping_list",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("shopping_list deleted successfully")
                resp.success()
            else:
                logger.error(f'''Failed to delete shopping_list: {
                    resp.status_code
                    }''')
                resp.failure("Failed to delete shopping_list")

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
        with self.client.put(
            url=f"/api/jared/shopping_list/{shopping_list['id']}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"shopping_list {shopping_list['id']} updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update shopping_list {shopping_list['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update shopping_list by id")

