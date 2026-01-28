import requests
import allure
from .endpoint import Endpoint


class GetMeme(Endpoint):

    @allure.step('Get a meme')
    def get_meme_by_id(self, meme_id):
        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.get(f"{self.url}/{meme_id}", headers=headers, timeout=5)
        return self.response

    @allure.step('Get all memes')
    def get_all_memes(self):

        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.get(self.url, headers=headers, timeout=5)
        return self.response
