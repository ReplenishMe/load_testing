import os
import requests
import time
import random
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    fetch_one,
    generate_text,
    generate_lp_id,
    fetch_one_stack
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestLicenseplates(FastHttpUser):
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
    def licenseplate_made(self):
        production_order = fetch_one('production_order')
        licenseplate_ids = generate_lp_id(1)
        stack_id = fetch_one_stack('stack')
        payload = {
            "production_order_id": production_order['id'],
            "lp_id": licenseplate_ids,
            "stack_id": stack_id['stack_id'],
            "quantity": 1,
        }
        with self.client.post(
            url="/api/jared/license_plates/made",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("Licenseplate made created successfully")
                resp.success() 
            else:
                logger.error(
                    f"Failed to create licenseplate made: {
                        resp.status_code
                        }"
                    )
                resp.failure(
                    "Failed to create licenseplate made"
                    )
  
    @task(1)
    def licenseplate_made_many(self):
        licenseplate = generate_lp_id(5)
        production_order_id_str = os.getenv("production_order_id")
        production_order_id = production_order_id_str.split(",")
        production_order_id = random.choice(production_order_id)
        payload = {
                    "production_order_id": production_order_id,
                    "lp_ids": licenseplate,
                    "quantity": 5
                }
        with self.client.post(
            url="/api/jared/license_plates/made_many",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 202:
                logger.info("Licenseplate made many requested successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to create licenseplate made many task id: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to create licenseplate made many task id")

    @task(1)
    def licenseplate_move(self):
        licenseplates_str = os.getenv("licenseplates")
        licenseplates = licenseplates_str.split(",")  # now it's a list
        licenseplate = random.choice(licenseplates)
        destination_id_str = os.getenv("destination_id")
        destination_id = destination_id_str.split(",")
        destination_id = random.choice(destination_id)
        users_str = os.getenv("users_id")
        users = users_str.split(",") 
        users = random.choice(users)
        payload = {
                "dest_location_id": destination_id,
                "license_plate_id": licenseplate,
                "user_id": users
            }
        with self.client.post(
            url="/api/jared/license_plates/move",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            time.sleep(5)
            message_ok = resp.json()['message'] == "license plate move created"
            if message_ok and resp.status_code == 200:
                logger.info(
                    "license plate move transaction created successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to create licenseplate move: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to create licenseplate move task id")

    @task(1)
    def licenseplate_move_many(self):
        licenseplates_str = os.getenv("licenseplates")
        licenseplates = licenseplates_str.split(",")  # now it's a list
        licenseplates = random.sample(licenseplates, 5)
        destination_id_str = os.getenv("destination_id")
        destination_id = destination_id_str.split(",")
        destination_id = random.choice(destination_id)
        users_str = os.getenv("users_id")
        users = users_str.split(",") 
        users = random.choice(users)
        payload = {
                "dest_location_id": destination_id,
                # "user_id": users,
                "license_plate_ids": licenseplates
            }
        with self.client.post(
            url="/api/jared/license_plates/move_many",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 202:
                logger.info(
                    "license plate move many transaction created successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to create licenseplate move many task id: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to create licenseplate move many task id")

    # @task(1)
    # def licenseplate_create(self):
    #     licenseplate = generate_lp_id()
    #     product = fetch_one('product')
    #     payload = {
    #             "lp_id": licenseplate,
    #             "product_id": product['id'],
    #             "quantity": 1
    #             }
    #     with self.client.post(
    #         url="/api/jared/license_plates",
    #         headers=self.default_headers,
    #         json=payload,
    #         catch_response=True
    #     ) as resp:
    #         if resp.status_code == 200:
    #             logger.info(
    #                 "licenseplate task id recieved successfully"
    #                 )
    #             resp.success()
    #         else:
    #             logger.error(
    #                 f"Failed to create licenseplate task id: {
    #                     resp.status_code
    #                     }"
    #                 )
    #             resp.failure("Failed to create licenseplate task id")

    @task(1)
    def licenseplate_comment(self):
        message = generate_text()
        lp = fetch_one('license_plate')
        payload = {
                "message": message
                }
        with self.client.post(
            url=f"/api/jared/license_plates/{lp['id']}/comment",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"licenseplate {lp['id']} comment updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update comment for licenseplate {lp['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update comment")

    @task(1)
    def get_licenseplate_id(self):
        lp = fetch_one('license_plate')
        with self.client.get(
            url=f"/api/jared/license_plates/{lp['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"licenseplate id {lp['id']} data fetched successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch licenseplate id {lp['id']} data: {
                        resp.status_code
                        }"
                    )
                resp.failure(
                    f"Failed to fetch licenseplate id {lp['id']} data"
                    )

    @task(1)
    def get_licenseplate_activities(self):
        lp = fetch_one('license_plate')
        with self.client.get(
            url=f"/api/jared/license_plates/{lp['id']}/activities",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''licenseplate id {
                                lp['id']
                                } activity data fetched successfully'''
                )
                resp.success()
            else:
                logger.error(
                    f'''Failed to fetch licenseplate id {
                                                        lp['id']
                                                        } activity data: {
                                                        resp.status_code
                                                        }'''
                    )
                resp.failure("Failed to fetch licenseplate id activity data")

    @task(1)
    def get_licenseplate_lookup(self):
        lp = fetch_one('license_plate')
        with self.client.get(
            url=f"/api/jared/license_plates/lookup?lp_id={lp['lp_id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''licenseplate id {
                        lp['id']
                        } lookup data fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch licenseplate id lookup data: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to fetch licenseplate id lookup data")
