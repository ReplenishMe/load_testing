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
    def create_user(self):
        name = generate_text(4)
        passwd = generate_text(5)
        payload = {
                    "email": f"{name}@gmail.com",
                    "password": f"{passwd}12@#"
                }
        with self.client.post(
            url="/api/jared/users",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("user created successfully")
                resp.success()
            else:
                logger.error(f"Failed to create user: {resp.status_code}")
                resp.failure("Failed to create user")
     
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
        with self.client.post(
            url="/api/jared/users/report",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 202:
                logger.info(
                    f'''user report generated successfully task id {
                        resp.json()['data']['task_id']
                        }''')
                resp.success()
            else:
                logger.error(f'''Failed to generate user report : {
                    resp.status_code
                    }''')
                resp.failure("Failed to generate user")

    # @task(1)                                      
    # def get_user_report(self):
    #     now = datetime.now(timezone.utc)
    #     start = now.replace(hour=18, minute=30, second=00, microsecond=000)
    #     end = start + timedelta(days=1)
    #     # start_str = start.strftime('%Y-%m-%d')
    #     # end_str = end.strftime('%Y-%m-%d')
    #     with self.client.get(
    #         url=f'''/api/jared/users/report?start_date={
    #             start}
    #             &end_date={
    #                 end
    #                 }''',
    #         headers=self.default_headers,
    #         catch_response=True
    #     ) as resp:
    #         if resp.status_code == 202:
    #             logger.info(f"user report fetched successfully task id")
    #             resp.success()
    #         else:
    #             logger.error(f"Failed to fetch user report")
    #             resp.failure("Failed to fetch user")       

    @task(1)                                      
    def user_invite(self):
        payload = {"email": "omni@gmail.com"}
        with self.client.post(
            url="/api/jared/users/invite",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("user invite mail sent successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to sent  invite mail : {resp.status_code}"
                    )
                resp.failure("Failed to sent invite mail")      

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
        with self.client.post(
            url="/api/jared/users/user-logs",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("user-logs created successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to create user-logs : {resp.status_code}"
                    )
                resp.failure("Failed to create user-logs")    

    @task(1)                                      
    def get_user_logs(self):
        user = fetch_one('user')
        with self.client.get(
            url=f"/api/jared/users/user-logs?user={user['person_id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("user-logs fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch user-logs : {resp.status_code}")
                resp.failure("Failed to fetch user-logs")                                  
    
    @task(1)
    def get_user_active(self):
        with self.client.get(
            url="/api/jared/users?include_inactive=true",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("active user fetched successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch active user : {resp.status_code}"
                    )
                resp.failure("Failed to fetch active user")
    
    @task(1)
    def get_user_id(self):
        user = fetch_one('user')
        with self.client.get(
            url=f"/api/jared/users/?user_id={user['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(f"user id {user['id']} fetched successfully")
                resp.success()
            else:
                logger.error(f'''Failed to fetch user id {user['id']}: {
                    resp.status_code
                    }''')
                resp.failure("Failed to fetch user")
    
    @task(1)
    def get_users(self):
        user = fetch_one('user')
        with self.client.get(
            url=f"/api/jared/users/{user['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("user fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch user : {resp.status_code}")
                resp.failure("Failed to fetch user")         
    
    @task(1)
    def get_locations_lookup(self):
        user = fetch_one('user')
        with self.client.get(
            url=f"/api/jared/users/lookup/?person_id={user['person_id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(f'''user person id {
                    user['person_id']
                    } fetched successfully''')
                resp.success()
            else:
                logger.error(
                    f'''Failed to fetch user person id 
                    {user['person_id']} :{resp.status_code}'''
                    )
                resp.failure("Failed to fetch user person id")    
    
    # @task(1)
    # def get_locations_report(self):
    #     loc = fetch_one('location')
    #     now = datetime.now(timezone.utc)
    #     start = now.replace(hour=18, minute=30, second=00, microsecond=000)
    #     end = start + timedelta(days=1)

    #     start_str = start.strftime('%Y-%m-%dT%H:%M-%S.000Z')
    #     end_str = end.strftime('%Y-%m-%dT%H:%M-%S.000Z')

    #     with self.client.get(
    #         url=f"api/jared/users/report/?start_date={start_str}&end_date={end_str}&page=1&per_page=10",
    #         headers=self.default_headers,
    #         catch_response=True
    #     ) as resp:
    #         if resp.status_code == 200:
    #             logger.info(
    #                         "report generated successfully"
    #                         )
    #         else:
    #             resp.failure("report not generated")
    
    @task(1)
    def change_user_roles(self):
        user = fetch_one('user')
        payload = {
                    "role_ids": [
                        40
                    ]
                }
        with self.client.post(
            url=f"/api/jared/users/{user['id']}/roles",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(f"user {user['id']} roles changed successfully")
                resp.success()
            else:
                logger.error(f'''Failed to change user {user['id']} roles : {
                    resp.status_code
                    }''')
                resp.failure("Failed to change user roles")

    @task(1)
    def get_roles(self):
        with self.client.get(
            url="/api/jared/roles",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("roles fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch roles : {resp.status_code}")
                resp.failure("Failed to fetch roles")          