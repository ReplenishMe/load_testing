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
        response = self.client.post(
            url="/auth/default/system/login",
            headers={"Accept-Encoding": "gzip, deflate, br"},
            data=payload
            )
        response.raise_for_status()
        token = response.json()['data']['access_token']

        self.default_headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Encoding": "gzip, deflate, br",
            }
        self._slug = os.getenv('ORG_SLUG')
    
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
        self.client.post(
            url=f"/api/{self._slug}/lim",
            headers=self.default_headers,
            json=payload
        )
  
    @task(1)
    def get_learning(self):
        self.client.get(
            url=f"/api/{self._slug}/lim",
            headers=self.default_headers
        )

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
        self.client.put(
            url=f"/api/{self._slug}/lim/{lim_id}",
            headers=self.default_headers,
            json=payload
        )
    
    @task(1)
    def get_learning_id(self):
        lim_str = os.getenv("lim_ids")
        lim_id = lim_str.split(",")  # now it's a list
        lim_id = random.choice(lim_id)
        self.client.get(
            url=f"/api/{self._slug}/lim/{lim_id}",
            headers=self.default_headers
        )
    
    @task(1)
    def delete_learning_id(self):
        lim_str = os.getenv("lim_ids")
        lim_id = lim_str.split(",")  # now it's a list
        lim_id = random.choice(lim_id)
        self.client.delete(
            url=f"/api/{self._slug}/lim/{lim_id}",
            headers=self.default_headers
        )