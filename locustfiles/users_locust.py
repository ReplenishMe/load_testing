import os
import requests
import logging
from datetime import datetime, timedelta, timezone
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


class LoadTestUsers(FastHttpUser):
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
    def create_user(self):
        name = generate_text(4)
        passwd = generate_text(5)
        payload = {
                    "email": f"{name}@gmail.com",
                    "password": f"{passwd}12@#"
                }
        self.client.post(
            url=f"/api/{self._slug}/users",
            headers=self.default_headers,
            json=payload
        )
     
    @task(1)                                      
    def user_report(self):
        now = datetime.now(timezone.utc)
        start = now.replace(hour=18, minute=30, second=00, microsecond=000)
        end = start + timedelta(days=1)
        start_str = start.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        payload = {
                    "email": "omni@gmail.com",
                    "end_date": end_str,
                    "start_date": start_str
                }
        self.client.post(
            url=f"/api{self._slug}/users/report",
            headers=self.default_headers,
            json=payload
        )

    # @task(1)                                      
    # def get_user_report(self):
    #     now = datetime.now(timezone.utc)
    #     start = now.replace(hour=18, minute=30, second=00, microsecond=000)
    #     end = start + timedelta(days=1)
    #     # start_str = start.strftime('%Y-%m-%d')
    #     # end_str = end.strftime('%Y-%m-%d')
            # self.client.get(
    #         url=f'''/api/{self._slug}/users/report?start_date={
    #             start}
    #             &end_date={
    #                 end
    #                 }''',
    #         headers=self.default_headers
    #     )  

    @task(1)                                      
    def user_invite(self):
        payload = {"email": "omni@gmail.com"}
        self.client.post(
            url=f"/api/{self._slug}/users/invite",
            headers=self.default_headers,
            json=payload
        )     

    @task(1)                                      
    def create_user_logs(self):
        user = fetch_one('user')
        now = datetime.now(timezone.utc)
        start = now.replace(hour=18, minute=30, second=00, microsecond=000)
        end = start + timedelta(days=1)
        start_str = start.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        payload = {
                "user": user['id'],
                "page": "1",
                "stringNote": "abc",
                "id": 0,
                "created_at": start_str,
                "updated_at": end_str
                }
        self.client.post(
            url=f"/api/{self._slug}/users/user-logs",
            headers=self.default_headers,
            json=payload
        )   

    @task(1)                                      
    def get_user_logs(self):
        user = fetch_one('user')
        self.client.get(
            url=f"/api/{self._slug}/users/user-logs?user={user['person_id']}",
            headers=self.default_headers
        )                                 
    
    @task(1)
    def get_user_active(self):
        self.client.get(
            url=f"/api/{self._slug}/users?include_inactive=true",
            headers=self.default_headers
        )
    
    @task(1)
    def get_user_id(self):
        user = fetch_one('user')
        self.client.get(
            url=f"/api/{self._slug}/users/?user_id={user['id']}",
            headers=self.default_headers
        )
    
    @task(1)
    def get_users(self):
        user = fetch_one('user')
        self.client.get(
            url=f"/api/{self._slug}/users/{user['id']}",
            headers=self.default_headers
        )     
    
    @task(1)
    def get_locations_lookup(self):
        user = fetch_one('user')
        self.client.get(
            url=f"/api/{self._slug}/users/lookup/?person_id={user['person_id']}",
            headers=self.default_headers
        )
            
    # @task(1)
    # def get_locations_report(self):
    #     loc = fetch_one('location')
    #     now = datetime.now(timezone.utc)
    #     start = now.replace(hour=18, minute=30, second=00, microsecond=000)
    #     end = start + timedelta(days=1)

    #     start_str = start.strftime('%Y-%m-%dT%H:%M-%S.000Z')
    #     end_str = end.strftime('%Y-%m-%dT%H:%M-%S.000Z')

    #     self.client.get(
    #         url=f"/api/{self._slug}/users/report/?start_date={start_str}&end_date={end_str}&page=1&per_page=10",
    #         headers=self.default_headers
    #     )
    
    @task(1)
    def change_user_roles(self):
        user = fetch_one('user')
        payload = {
                    "role_ids": [
                        40
                    ]
                }
        self.client.post(
            url=f"/api/{self._slug}/users/{user['id']}/roles",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def get_roles(self):
        self.client.get(
            url=f"/api/{self._slug}/roles",
            headers=self.default_headers
        )       