import requests
import allure

from .endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step('Delete a meme')
    def delete_meme_by_id(self, meme_id):

        headers = {
            'Authorization': f'{self.token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.delete(f'{self.url}/{meme_id}', headers=headers)

        return self.response
