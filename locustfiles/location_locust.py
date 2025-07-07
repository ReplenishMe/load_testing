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
    def create_location(self):
        name = generate_text()
        payload = {
                "name": name,
            }
        with self.client.post(
            url="/api/jared/locations",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("location created successfully")
                resp.success()
            else:
                logger.error(f"Failed to create location: {resp.status_code}")
                resp.failure("Failed to create location")

    @task(1)
    def get_locations_id(self):
        loc = fetch_one('location')
        with self.client.get(
            url=f"/api/jared/locations/{loc['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(f"location id {loc['id']} fetched successfully")
                resp.success()
            else:
                logger.error(
                    f"Failed to fetch location id {loc['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to fetch location id")
    
    @task(1)
    def get_locations(self):
        with self.client.get(
            url="/api/jared/locations",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("location fetched successfully")
                resp.success()
            else:
                logger.error(f"Failed to fetch location: {resp.status_code}")
                resp.failure("Failed to fetch location") 
    
    @task(1)
    def get_locations_lookup(self):
        loc = fetch_one('location')
        with self.client.get(
            url=f"/api/jared/locations/lookup?beacon_id={loc['beacon_id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''location beacon id {
                        loc['beacon_id']
                        } lookup fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(f'''Failed to fetch location beacon id {
                            loc['beacon_id']
                            } lookup : {
                            resp.status_code
                            }
                        ''')
                resp.failure("Failed to fetch location beacon lookup")
    
    # @task(1)
    # def location_email_logs(self):
    #     with self.client.post(
    #         url="/api/jared/locations/email_logs",
    #         headers=self.default_headers,
    #         catch_response=True
    #     ) as resp:
    #         if resp.status_code == 200:
    #             resp.success()
    #         else:
    #             resp.failure("api failed fetched location lookup")       
    
    @task(1)
    def get_locations_report(self):
        loc = fetch_one('location')
        now = datetime.now(timezone.utc)
        start = now.replace(hour=18, minute=30, second=00, microsecond=000)
        end = start + timedelta(days=1)
        start_str = start.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.000Z')

        with self.client.get(
            url=f"/api/jared/locations/{loc['id']}/report?page=1&start_date={
                start_str
                }&end_date={
                    end_str
                    }",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''location id {
                        loc['id']
                        } lookup fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(f'''Failed to fetch location id {
                            loc['id']
                            } lookup : {
                            resp.status_code
                            }
                        ''')
                resp.failure("Failed to fetch location id report")