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


class LoadTestLearning(FastHttpUser):
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
    def create_learning(self):
        payload = {
                    "description": "",
                    "email": "loadtest@gmail.com",
                    "instructions": "",
                    "pick_type": "TRAINING",
                    "thumbnail_url": "https://s3-fileuploads.s3.us-west-2.amazonaws.com/uploads/fd5ca25d502d447a8bd00a74db78fbc8.jpg",
                    "title": "Learn",
                    "video_url": "https://s3-fileuploads.s3.us-west-2.amazonaws.com/uploads/98e53fd981764fe4b420d5e6044a9ed2.webm",
                    "visibility": "PUBLIC"
                }
        with self.client.post(
            url="/api/jared/lim",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("lim created successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to create lim: {resp.status_code}"
                    )
                resp.failure("Failed to create lim")
  
    @task(1)
    def get_learning(self):
        with self.client.get(
            url="api/jared/lim",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("lim fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch lim: {resp.status_code}")
                resp.failure("Failed to fetch lim")

    @task(1)                                      
    def update_learning_id(self):
        lim_str = os.getenv("lim_ids")
        lim_id = lim_str.split(",")  # now it's a list
        lim_id = random.choice(lim_id)
        payload = {
                    "description": "",
                    "email": "updatedemo@gmail.com",
                    "instructions": "",
                    "pick_type": "TRAINING",
                    "thumbnail_url": "https://s3-fileuploads.s3.us-west-2.amazonaws.com/uploads/fd5ca25d502d447a8bd00a74db78fbc8.jpg",
                    "title": "Learn",
                    "video_url": "https://s3-fileuploads.s3.us-west-2.amazonaws.com/uploads/98e53fd981764fe4b420d5e6044a9ed2.webm",
                    "visibility": "PUBLIC"
                }
        with self.client.put(
            url=f"/api/jared/lim/{lim_id}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"learning {lim_id['id']} updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update lim {lim_id['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update lim by ID")
    
    @task(1)
    def get_learning_id(self):
        lim_str = os.getenv("lim_ids")
        lim_id = lim_str.split(",")  # now it's a list
        lim_id = random.choice(lim_id)
        with self.client.get(
            url=f"/api/jared/lim/{lim_id}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"lim {lim_id} fetched successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch lim {lim_id}: {
                        resp.status_code
                        }"
                )
                resp.failure("Failed to fetch lim by ID")
    
    @task(1)
    def delete_learning_id(self):
        lim_str = os.getenv("lim_ids")
        lim_id = lim_str.split(",")  # now it's a list
        lim_id = random.choice(lim_id)
        with self.client.delete(
            url=f"/api/jared/lim/{lim_id}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"lim {lim_id['id']} deleted successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to delete lim {lim_id}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to lim by ID")