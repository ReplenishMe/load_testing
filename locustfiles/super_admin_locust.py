import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    generate_text,
    fetch_one_org
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestSuperAdmin(FastHttpUser):
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
    def create_super_admin(self):
        org = generate_text()
        name = generate_text(4)
        passwd = generate_text(5)
        payload = {
                "name": f"abc_{name}",
                "email": f"abc_{name}@gmail.com",
                "password": passwd,
                "org_name": org,
                "org_slug": org,
                "org_address": org
                }
        with self.client.post(
            url="/api/jared/__super_admin__/setup-org",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("super_admin created successfully")
                resp.success()
            else:
                logger.error(f'''Failed to create super_admin: {
                    resp.text
                    }''')
                resp.failure("Failed to create super_admin")

    @task(0)
    def super_admin_update_json(self):
        org = fetch_one_org('organization')
        payload = {
                "org_id": org['id'],
                "template": None
                }
        with self.client.post(
            url="/api/jared/__super_admin__/update-json",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"super_admin json updated created successfully task id {
                        resp.json()['data']['task_id']
                        }"
                    )
                resp.success()
            else:
                logger.error(f'''Failed to update super_admin json: {
                    resp.status_code
                    }''')
                resp.failure("Failed to update super_admin json")