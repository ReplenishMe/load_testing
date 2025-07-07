import os
import random
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestPick(FastHttpUser):
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
    def create_pick(self):
        docid_str = os.getenv("docid")
        docid = docid_str.split(",") 
        docid = random.choice(docid)
        payload = {
                "docid": docid,
                "pick_type": "new",
                }
        with self.client.post(
            url="/api/jared/pick",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("picks created successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to create picks: {resp.status_code}"
                    )
                resp.failure("Failed to create picks")
  
    @task(1)
    def get_pick(self):
        with self.client.get(
            url="api/jared/pick",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("pick fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch pick: {resp.status_code}")
                resp.failure("Failed to fetch pick")
    
    @task(1)                                      
    def update_pick_id(self):
        docid_str = os.getenv("docid")
        docid = docid_str.split(",")  
        docid = random.choice(docid)
        pick_str = os.getenv("pick_id")
        pick = pick_str.split(",") 
        pick = random.choice(pick)
        payload = {
                "docid": docid,
                "pick_type": "new",
                }
        with self.client.put(
            url=f"/api/jared/pick/{pick}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"pick {pick} updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update pick {pick}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update pick by ID")
    
    @task(1)
    def get_pick_id(self):
        pick_str = os.getenv("pick_id")
        pick = pick_str.split(",")  
        pick = random.choice(pick)
        with self.client.get(
            url=f"/api/jared/pick/{pick}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"pick {pick} fetched successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch pick {pick}: {
                        resp.status_code
                        }"
                )
                resp.failure("Failed to fetch pick by ID")
    
    @task(1)
    def delete_pick_id(self):
        pick_str = os.getenv("pick_id")
        pick = pick_str.split(",")  
        pick = random.choice(pick)
        with self.client.delete(
            url=f"/api/jared/pick/{pick}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"pick {pick} deleted successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to delete pick {pick}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to delete pick by id")