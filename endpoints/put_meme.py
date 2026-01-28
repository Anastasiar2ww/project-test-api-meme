import requests
import allure

from .endpoint import Endpoint


class UpdateMeme(Endpoint):

    @allure.step('Update a meme')
    def put_meme_by_id(self, body, meme_id):

        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }

        self.response = requests.put(f'{self.url}/{meme_id}', json=body, headers=headers)
        return self.response
