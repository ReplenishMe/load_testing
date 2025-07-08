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


class LoadTestLocation(FastHttpUser):
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
    def create_location(self):
        name = generate_text()
        payload = {
                "name": name,
            }
        self.client.post(
            url=f"/api/{self._slug}/locations",
            headers=self.default_headers,
            json=payload
        )

    @task(1)
    def get_locations_id(self):
        loc = fetch_one('location')
        print(loc)
        self.client.get(
            url=f"/api/{self._slug}/locations/{loc['id']}",
            headers=self.default_headers
        )
    
    @task(1)
    def get_locations(self):
        self.client.get(
            url=f"/api/{self._slug}/locations",
            headers=self.default_headers
        )
    
    @task(1)
    def get_locations_lookup(self):
        loc = fetch_one('location')
        self.client.get(
            url=f"/api/{self._slug}/locations/lookup?beacon_id={loc['beacon_id']}",
            headers=self.default_headers
        )
    
    # @task(1)
    # def location_email_logs(self):
    #     self.client.post(
    #         url="/api/jared/locations/email_logs",
    #         headers=self.default_headers
    #     )
    
    @task(1)
    def get_locations_report(self):
        loc = fetch_one('location')
        now = datetime.now(timezone.utc)
        start = now.replace(hour=18, minute=30, second=00, microsecond=000)
        end = start + timedelta(days=1)
        start_str = start.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.000Z')

        self.client.get(
            url=f"/api/{self._slug}/locations/{loc['id']}/report?page=1&start_date={
                start_str
                }&end_date={
                    end_str
                    }",
            headers=self.default_headers
        )