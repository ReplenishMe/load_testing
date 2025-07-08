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
        self.client.post(
            url=f"/api/{self._slug}/__super_admin__/setup-org",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def super_admin_update_json(self):
        org = fetch_one_org('organization')
        payload = {
                "org_id": org['id'],
                "template": None
                }
        self.client.post(
            url=f"/api/{self._slug}/__super_admin__/update-json",
            headers=self.default_headers,
            json=payload
        )