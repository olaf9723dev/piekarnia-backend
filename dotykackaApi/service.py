import pprint

import requests

from piekarniaApi import settings


class DotykackaApiService:

    def __init__(self, refresh_token, cloud_id, api_url):
        self.refresh_token = refresh_token
        self.cloud_id = cloud_id
        self.api_url = api_url
        self.access_token = None

    def authenticate(self):
        headers = {'Authorization': f'User {self.refresh_token}'}
        result = requests.post(
            self.api_url,
            json={'_cloudId': self.cloud_id},
            headers=headers)
        if result.status_code == 201:
            self.access_token = result.json()['accessToken']
            return True
        else:
            result_json = result.json()
            raise Exception(
                f'DotykackaApi auth exception: {result_json["status"]}, {result_json["message"]}'
            )

    def get_categories(self, limit):
        if not self.access_token:
            raise Exception('DotykackaApi not authenticated')

        headers = {'Authorization': f'Bearer {self.access_token}'}
        result = requests.get(f'{settings.DOTYKACKA_URL}{self.cloud_id}/categories?limit={limit}', headers=headers)

        if result.status_code == 200:
            return result.json()
        else:
            result_json = result.json()
            raise Exception(
                f'DotykackaApi auth exception: {result_json["status"]}, {result_json["message"]}'
            )

    def get_products(self, page, limit):
        if not self.access_token:
            raise Exception('DotykackaApi not authenticated')

        headers = {'Authorization': f'Bearer {self.access_token}'}
        result = requests.get(f'{settings.DOTYKACKA_URL}{self.cloud_id}/products?page={page}&limit={limit}', headers=headers)

        if result.status_code == 200:
            pprint.pprint(result.json())
            return result.json()
        else:
            result_json = result.json()
            raise Exception(
                f'DotykackaApi auth exception: {result_json["status"]}, {result_json["message"]}'
            )
