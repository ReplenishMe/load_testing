import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    fetch_one,
    fetch_one_stack,
    fetch_stack_lp
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestStack(FastHttpUser):
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
    def get_stack(self):
        with self.client.get(
            url="/api/jared/stack",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("stack fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch stack: {resp.status_code}")
                resp.failure("Failed to fetch stack")
    
    @task(1)
    def stack_start(self):
        loc = fetch_one('location')
        production_order = fetch_one('production_order')
        payload = {
                "location_id": loc['id'],
                "production_order_id": production_order['docid']
                }
        with self.client.post(
            url="/api/jared/stack/start",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("stack close requested successfully")
                resp.success()
            else:
                logger.error(f'''Failed to request stack close: {
                    resp.status_code
                    }''')
                resp.failure("Failed to request stack close") 

    @task(1)
    def close_stack(self):
        stack = fetch_one_stack('stack')
        stack_lp = fetch_stack_lp(
            'licenseplates', stack["product_id"], stack["location_id"]
        )
        payload = {
            "item_count": 0,
            "qrs": [stack_lp],
            "stack_id": stack['id']
            }
        with self.client.post(
            url="/api/jared/stack/close",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("stack close requested successfully")
                resp.success()
            else:
                logger.error(f'''Failed to request stack close: {
                    resp.status_code
                    }''')
                resp.failure("Failed to request stack close") 


                     
    
