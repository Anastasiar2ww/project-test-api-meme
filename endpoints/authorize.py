import requests
import allure
from .endpoint import Endpoint


class Authorize(Endpoint):

    @allure.step('Authorize user')
    def authorize_user(self, username):
        auth_data = {
            "name": username
        }

        self.response = requests.post(self.auth_url, json=auth_data)
        return self.response

    @allure.step('Check token is alive')
    def check_token(self, token):
        self.response = requests.get(f'{self.auth_url}/{token}')
        return self.response
