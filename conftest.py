import pytest
import requests
import datetime

from endpoints.create_meme import CreateMeme
from endpoints.put_meme import UpdateMeme
from endpoints.get_meme import GetMeme
from endpoints.delete_meme import DeleteMeme
from endpoints.authorize import Authorize


@pytest.fixture()
def authorize_endpoint():
    return Authorize()


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def update_meme_endpoint():
    return UpdateMeme()


@pytest.fixture()
def get_meme_endpoint():
    return GetMeme()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture(scope="session")
def auth_token():
    auth_url = 'http://memesapi.course.qa-practice.com/authorize'
    name = f"test_user_{datetime.datetime.now().strftime('%Y%m%d')}"
    response = requests.post(auth_url, json={"name": name})
    token = response.json()['token']
    return token


@pytest.fixture(autouse=True)
def inject_token_to_all_endpoints(auth_token, create_meme_endpoint, get_meme_endpoint,
                                  update_meme_endpoint, delete_meme_endpoint):
    create_meme_endpoint.token = auth_token
    get_meme_endpoint.token = auth_token
    update_meme_endpoint.token = auth_token
    delete_meme_endpoint.token = auth_token


@pytest.fixture()
def create_meme_for_delete(create_meme_endpoint):

    body = {
    "url": "https://habrastorage.org/r/w1560/getpro/habr/upload_files/baf/b76/3a5/bafb763a54d1cd106a9493c2862ad757.png",
    "text": "test meme",
    "tags": ["fun", "QA"],
    "info": {"text_1": "meme research", "text_2": "QA"}
    }

    response = create_meme_endpoint.create_new_meme(body)

    yield response.json()['id']


@pytest.fixture()
def meme_id(create_meme_endpoint, delete_meme_endpoint):

    body = {
    "url": "https://habrastorage.org/r/w1560/getpro/habr/upload_files/baf/b76/3a5/bafb763a54d1cd106a9493c2862ad757.png",
    "text": "test meme",
    "tags": ["fun", "QA"],
    "info": {"text_1": "meme research", "text_2": "QA"}
        }

    create_meme_endpoint.create_new_meme(body)

    meme_id = create_meme_endpoint.get_meme_id()

    yield meme_id

    delete_meme_endpoint.delete_meme_by_id(meme_id)
