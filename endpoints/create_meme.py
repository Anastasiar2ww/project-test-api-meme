import requests
import allure
from .endpoint import Endpoint


class CreateMeme(Endpoint):

    @allure.step('Create new meme')
    def create_new_meme(self, body):

        token = self.token

        headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.post(self.url, json=body, headers=headers)
        return self.response
