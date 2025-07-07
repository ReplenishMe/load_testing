import os
import requests
import logging
from dotenv import load_dotenv
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
from db import (
    fetch_one,
    generate_text,
    generate_digit
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LoadTestProduct(FastHttpUser):
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
    def create_products(self):
        payload = {
                    "part_number": generate_digit(),
                    "name": generate_text(),
                    "description": generate_text(),
                    "preferred_vendor_id": 1,
                    "preferred_vendor_part_number": generate_digit(),
                    "erp_part_number": generate_digit(),
                    "uom": "0",
                    "is_external": True,
                    "active": True
                    }    
        with self.client.post(
            url="/api/jared/products",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info("product created successfully")
                resp.success()
            else:
                logger.error(f"Failed to create product: {resp.status_code}")
                resp.failure("Failed to create product")
    
    @task(1)
    def get_products(self):
        with self.client.get(
            url="/api/jared/products",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info('product fetched successfully')
                resp.success()
            else:
                logger.error(f'Failed to fetch product: {resp.status_code}')
                resp.failure("Failed to fetch product id")    

    @task(1)
    def get_product_by_id(self):
        product = fetch_one('product')
        with self.client.get(
            url=f"/api/jared/products/{product['id']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''product id {
                        product['id']
                        } fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(f'''Failed to fetch product id {
                            product['id']
                            }: {
                            resp.status_code
                            }
                        ''')
                resp.failure("Failed to fetch product id")            
  
    @task(1)               
    def update_product_id(self):
        product = fetch_one('product')
        name = generate_text()
        payload = {
                   "description": name,
                   "erp_part_number": "",
                   "name": name,
                   "part_number": name,
                }
        with self.client.put(
            url=f"/api/jared/products/{product['id']}",
            headers=self.default_headers,
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f"product {product['id']} updated successfully"
                    )
                resp.success()
            else:
                logger.error(
                    f"Failed to update product {product['id']}: {
                        resp.status_code
                        }"
                    )
                resp.failure("Failed to update product by id")
    
    # @task(1)
    # def delete_product_id(self):
    #     product = fetch_one_asc('product')
    #     with self.client.delete(
    #         url=f"/api/jared/products/{product['id']}",
    #         headers=self.default_headers,
    #         catch_response=True
    #     ) as resp:
    #         if resp.status_code == 200:
    #             logger.info(
    #                 f"product {product['id']} deleted successfully"
    #                 )
    #             resp.success()
    #         else:
    #             logger.error(
    #                 f"Failed to delete product {product['id']}: {
    #                     resp.status_code
    #                     }"
    #                 )
    #             resp.failure("Failed to delete bin by id")
    
    @task(1)
    def get_product_by_partnumber(self):
        with self.client.get(
            url="/api/jared/products/partnumbers",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info('product part number lookup fetched successfully')
                resp.success()
            else:
                logger.error(f'''Failed to fetch product part number :{
                    resp.status_code
                    }''')
                resp.failure("Failed to fetch product part number")

    @task(1)
    def get_product_lookup(self):
        product = fetch_one('product')
        with self.client.get(
            url=f"/api/jared/products/lookup/?part_number={
                                            product['part_number']}",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'''product part number {
                        product['part_number']
                        } lookup fetched successfully'''
                    )
                resp.success()
            else:
                logger.error(f'''Failed to fetch product part number{
                            product['part_number']
                            }  lookup: {
                            resp.status_code
                            }
                        ''')
                resp.failure("Failed to fetch product part number lookup")

    # @task(1)
    # def get_product_by_name(self):
    #     product = fetch_all('product')
    #     with self.client.get(
    #         url=f"/api/jared/products/{product['name']}",
    #         headers=self.default_headers,
    #         catch_response=True
    #     ) as resp:
    #         if resp.status_code == 200:
    #             logger.info(
    #                 f'''product name {
    #                     product['name']
    #                     } fetched successfully'''
    #                 )
    #             resp.success()
    #         else:
    #             logger.error(f'''Failed to fetch product name {
    #                         product['name']
    #                         }: {
    #                         resp.status_code
    #                         }
    #                     ''')
    #             resp.failure("Failed to fetch product name")
    
    @task(1)
    def get_products_report(self):
        product = fetch_one('product')
        with self.client.get(
            url=f"/api/jared/products/{product['id']}/report",
            headers=self.default_headers,
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                logger.info(
                    f'product id {product['id']} report fetched successfully'
                    )
                resp.success()
            else:
                logger.error(f'''Failed to fetch product id {
                                                            product['id']
                                                            } report: {
                                                            resp.status_code
                                                            }''')
                resp.failure("Failed to fetch product id report")