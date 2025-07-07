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
    def create_production_orders(self):
        product = fetch_one('product')
        external_docid = generate_text(5)
        digit_qty = generate_digit(4)
        payload = {
                    "external_docid": external_docid,
                    "product_id": product['id'],
                    "requested_qty": digit_qty
                    }
        with self.client.post(
            url="/api/jared/production_orders",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("production order created successfully")
                resp.success()
            else:
                logger.error(
                    f'Failed to create production order: {resp.status_code}'
                    )
                resp.failure("Failed to create production order")

    @task(1)
    def get_production_orders(self):
        with self.client.get(
            url="/api/jared/production_orders",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("production order fetched successfully")
                resp.success()
            else:
                logger.error(f'''Failed to fetch production order: {
                    resp.status_code
                    }''')
                resp.failure("Failed to fetch production order")
             
    @task(1)
    def get_production_orders_id(self):
        production_order = fetch_one('production_order')
        with self.client.get(
            url=f"/api/jared/production_orders/{production_order['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''production_order {
                        production_order['id']
                        } fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch production_order {
                        production_order['id']
                        }: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to fetch production_order by id")

    @task(1)
    def patch_production_orders_id(self):
        requested_qty = generate_digit(5)
        production_order = fetch_one('production_order')
        payload = {
                    "requested_qty": requested_qty,
                }
        with self.client.patch(
            url=f"/api/jared/production_orders/{production_order['id']}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''production_order {
                        production_order['id']
                        } patched successfully'''
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to patch production_order {
                        production_order['id']
                        }: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to patch production_order by id")  

    @task(1)
    def patch_production_orders_id_permissions(self):
        production_order = fetch_one('production_order')
        payload = {
                    "add": [2],
                    "remove": [4, 8, 16, 64, 32, 128]
                }
        with self.client.patch(
            url=f'''/api/jared/production_orders/{
                production_order['id']
                }/public_view_permissions''',
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''production_order {
                        production_order['id']
                        } permissions patched successfully'''
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to patch permissions of production_order {
                        production_order['id']
                        }: {
                        resp.status_code
                        }"
                    )
                resp.failure(
                    "Failed to patch permissions of production_order by id"
                )                    
  
    @task(1)
    def production_orders_email_report(self):
        payload = {"email": "shyamgundetin@gmail.com"}
        with self.client.post(
            url="/api/jared/production_orders/email_report",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 202:
                logger.info(
                    f'''production_order email report requested successfully:
                        task id {
                                resp.json()['data']['task_id']
                                }'''
                    )
                resp.success()
            else:
                logger.error("Failed to request production_order email report")
                resp.failure("Failed to request production_order email report")

    @task(1)
    def productionorder_status_report(self):
        production_order = fetch_one('production_order')
        with self.client.get(
            url=f"""/api/jared/production_orders/{
                production_order['id']
                }/status_report?page=1""",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    'production_order status report requested successfully'
                    )
                resp.success()
            else:
                logger.error("Failed to status report production_order")
                resp.failure("Failed to status report production_order")

    @task(1)
    def get_production_order_lookup(self):
        production_order = fetch_one('production_order')
        with self.client.get(
            url=f"/api/jared/production_orders/lookup?docid={
                production_order['docid']
                }",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''production_order docid {
                        production_order['docid']
                        } lookup fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(
                    f"""Failed to fetch production_order docid{
                        production_order['docid']
                        } lookup : {
                        resp.status_code
                        }"""
                    )
                resp.failure("Failed to fetch production_order by docid")

    @task(1)
    def get_production_orders_page(self):
        with self.client.get(
            url="/api/jared/production_orders?page=1&per_page=50",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info('production_order fetched successfully')
                resp.success()
            else:
                logger.error("Failed to fetch production_order")
                resp.failure("Failed to fetch production_order")

    @task(1)
    def get_production_orders_keyword(self):
        production_order = fetch_one('production_order')
        with self.client.get(
            url=f'''/api/jared/production_orders?keyword={
                production_order['external_docid']
                }&page=1&per_page=50''',
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    '''production_order with work order or partnumber 
                       fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(
                    '''Failed to fetch production_order with 
                       work order or partnumber'''
                    )
                resp.failure(
                    '''Failed to fetch production_order with 
                       work order or partnumber'''
                    )