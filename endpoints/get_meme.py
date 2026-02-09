import requests
import allure
from .endpoint import Endpoint
import pytest


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
        try:
            headers = {
                'Authorization': f'{self.token}',
                'Content-Type': 'application/json'
            }
            self.response = requests.get(self.url, headers=headers, timeout=5)
            return self.response
        except requests.exceptions.ConnectionError:
            pytest.fail("Ошибка соединения с сервером")

        except requests.exceptions.ReadTimeout:
            pytest.fail("Сервер не ответил за 5 секунд")
