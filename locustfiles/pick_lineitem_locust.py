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


class LoadTestPickLineitem(FastHttpUser):
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
    def create_pick_lineitem(self):
        payload = {
                "request_qity": 123,
                "fullfilled_qty": 100
                }
        with self.client.post(
            url="/api/jared/pick_lineitem",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("Pick Lineitems created successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to create Pick Lineitems: {resp.status_code}"
                    )
                resp.failure("Failed to create Pick Lineitems")
  
    @task(1)
    def get_pick_lineitem(self):
        with self.client.get(
            url="api/jared/pick_lineitem",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("Pick Lineitem fetched successfully")
                resp.success()
            else:
                logger.error(
                    f'''Failed to fetch Pick Lineitem: {
                        resp.status_code
                        }''')
                resp.failure("Failed to fetch Pick Lineitem")
    
    @task(1)                                      
    def update_pick_lineitem_id(self):
        pick_lineitem = fetch_one('Pick Lineitem')
        payload = {
                "request_qity": 123,
                "fullfilled_qty": 100
                }
        with self.client.put(
            url=f"/api/jared/Pick Lineitem/{pick_lineitem['id']}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"learning {pick_lineitem['id']} updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update Pick Lineitem {pick_lineitem['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update Pick Lineitem by ID")
    
    @task(1)
    def get_pick_lineitem_id(self):
        pick_lineitem = fetch_one('pick_lineitem')
        with self.client.get(
            url=f"/api/jared/Pick Lineitem/{pick_lineitem['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''Pick Lineitem {
                        pick_lineitem['id']
                        } fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch Pick Lineitem {pick_lineitem['id']}: {
                        resp.status_code
                        }"
                )
                resp.failure("Failed to fetch Pick Lineitem by ID")
    
    @task(1)
    def delete_pick_lineitem_id(self):
        pick_lineitem = fetch_one('pick_lineitem')
        with self.client.delete(
            url=f"/api/jared/Pick Lineitem/{pick_lineitem['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''Pick Lineitem {
                        pick_lineitem['id']
                        } deleted successfully'''
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to delete Pick Lineitem {pick_lineitem['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to delete Pick Lineitem by id")