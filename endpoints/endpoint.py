import allure
import requests


class Endpoint:
    url = 'http://memesapi.course.qa-practice.com/meme'
    auth_url = 'http://memesapi.course.qa-practice.com/authorize'
    token = None
    response = None

    @allure.step('Check status code is {expected_code}')
    def check_status_code(self, expected_code):
        assert expected_code == self.response.status_code

    @allure.step('Get meme_id')
    def get_meme_id(self):
        meme_id = self.response.json()['id']
        return meme_id

    @allure.step('Check meme_id is correct')
    def check_meme_id_is_correct(self, meme_id):
        assert self.response.json()['id'] == meme_id

    @allure.step('Check all fields are correct')
    def check_all_fields(self, expected_data):
        actual_data = self.response.json()

        for field in ['text', 'url', 'tags', 'info']:
            if field in expected_data:
                assert actual_data[field] == expected_data[field], f"Поле '{field}' не совпадает"

    @allure.step('Check field {field_name} value')
    def check_field_value(self, field_name, expected_value):
        actual_value = self.response.json().get(field_name)
        assert actual_value == expected_value

    @allure.step('Authorize user')
    def authorize(self, username):
        auth_data = {
            "name": username
        }
        self.response = requests.post(self.auth_url, json=auth_data)
        return self.response

    @allure.step('Check response contains list in {field_name}')
    def check_response_contains_list(self, field_name='data'):
        data = self.response.json()
        assert field_name in data
        assert isinstance(data[field_name], list)
        return data[field_name]

    @allure.step('Check response has field {field_name}')
    def check_response_has_field(self, field_name):
        data = self.response.json()
        assert field_name in data
        return data[field_name]
