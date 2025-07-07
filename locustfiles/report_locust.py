import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, constant
from locust.contrib.fasthttp import FastHttpUser
from db import fetch_one

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestReport(FastHttpUser):
    wait_time = constant(5)

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
    def order_report(self):
        production_order = fetch_one('production_order')
        payload = {
                    "order_id": production_order['id'],
                    "email": "shyamgundetin@gmail.com"
                }
        with self.client.post(
            url="/api/jared/reports/orders",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 202:
                logger.info(
                    f'order report requested successfully task id {
                        resp.json()['data']['task_id']
                        }'
                    )
                resp.success()
            else:
                logger.error("Failed to request order report")
                resp.failure(" to request order report")
     
    @task(1)                                      
    def everything_report(self):
        payload = {  
                    "email": "shyamgundetin@gmail.com"
                }
        with self.client.post(
            url="/api/jared/reports/everything_report",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'everything report requested successfully task id {
                        resp.json()['data']['task_id']
                        }'
                    )
                resp.success()
            else:
                logger.error("Failed to request everything report")
                resp.failure("Failed to request everything report")

    