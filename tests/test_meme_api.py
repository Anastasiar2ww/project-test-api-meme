import pytest
import requests

TEST_DATA = [

    {
    "url": "https://habrastorage.org/r/w1560/getpro/habr/upload_files/baf/b76/3a5/bafb763a54d1cd106a9493c2862ad757.png",
    "text": "test meme",
    "tags": ["fun", "QA"],
    "info": {"text_1": "meme research", "text_2": "QA"}
    }

]

TEST_DATA_UPDATE = [
    {
    "id": None,
    "url": "https://habrastorage.org/r/w1560/getpro/habr/upload_files/baf/b76/3a5/bafb763a54d1cd106a9493c2862ad757.png",
    "text": "test meme UPDATE",
    "tags": ["fun", "QA"],
    "info": {"text_1": "meme research", "text_2": "QA"}
    }
]

TEST_DATA_NEGATIVE = [
    {
    "url": "https://habrastorage.org/r/w1560/getpro/habr/upload_files/baf/b76/3a5/bafb763a54d1cd106a9493c2862ad757.png",
    "tags": ["fun", "QA"],
    "info": {"text_1": "meme research", "text_2": "QA"}
    },
    {
    "url": "https://habrastorage.org/r/w1560/getpro/habr/upload_files/baf/b76/3a5/bafb763a54d1cd106a9493c2862ad757.png",
    "text": "test meme",
    "tags": 1,
    "info": {"text_1": "meme research", "text_2": "QA"}
    }
]

TEST_DATA_AUTH = "test_user"

TEST_DATA_AUTH_WRONG = 123

WRONG_TOKEN = 'qwerty12345'


def test_authorize_basic(authorize_endpoint):
    authorize_endpoint.authorize_user(TEST_DATA_AUTH)
    authorize_endpoint.check_status_code(200)
    authorize_endpoint.check_field_value('user', TEST_DATA_AUTH)
    authorize_endpoint.check_response_has_field('token')


def test_authorize_wrong_value(authorize_endpoint):
    authorize_endpoint.authorize_user(TEST_DATA_AUTH_WRONG)
    authorize_endpoint.check_status_code(400)


def test_token_check(authorize_endpoint):
    authorize_endpoint.authorize_user("test")
    token = authorize_endpoint.response.json()['token']
    authorize_endpoint.check_token(token)
    authorize_endpoint.check_status_code(200)


def test_create_meme(create_meme_endpoint):
    data = TEST_DATA[0]
    create_meme_endpoint.create_new_meme(data)
    create_meme_endpoint.check_status_code(200)


def test_create_meme_without_field(create_meme_endpoint):
    data = TEST_DATA_NEGATIVE[0]
    create_meme_endpoint.create_new_meme(data)
    create_meme_endpoint.check_status_code(400)


def test_create_meme_incorrect_value(create_meme_endpoint):
    data = TEST_DATA_NEGATIVE[1]
    create_meme_endpoint.create_new_meme(data)
    create_meme_endpoint.check_status_code(400)


def test_create_meme_with_wrong_token(create_meme_endpoint):
    original_token = create_meme_endpoint.token
    create_meme_endpoint.token = WRONG_TOKEN
    data = TEST_DATA[0]
    create_meme_endpoint.create_new_meme(data)
    create_meme_endpoint.check_status_code(401)
    create_meme_endpoint.token = original_token


def test_get_meme(get_meme_endpoint, meme_id):
    get_meme_endpoint.get_meme_by_id(meme_id)
    get_meme_endpoint.check_status_code(200)
    get_meme_endpoint.check_field_value('id', meme_id)


def test_get_wrong_meme_id(get_meme_endpoint, meme_id):
    get_meme_endpoint.get_meme_by_id(0)
    get_meme_endpoint.check_status_code(404)


def test_all_memes(get_meme_endpoint):
    try:
        get_meme_endpoint.get_all_memes()
        get_meme_endpoint.check_status_code(200)
    except requests.exceptions.ConnectionError:
        pytest.fail("Ошибка соединения с сервером")
    except requests.exceptions.ReadTimeout:
        pytest.fail("Сервер не ответил за 5 секунд")


def test_all_memes_structure(get_meme_endpoint):
    try:
        get_meme_endpoint.get_all_memes()
        get_meme_endpoint.check_response_contains_list()
    except requests.exceptions.ConnectionError:
        pytest.fail("Ошибка соединения с сервером")
    except requests.exceptions.ReadTimeout:
        pytest.fail("Сервер не ответил за 5 секунд")


def test_update_meme(update_meme_endpoint, get_meme_endpoint, meme_id):
    update_data = TEST_DATA_UPDATE[0]
    update_data['id'] = meme_id
    update_meme_endpoint.put_meme_by_id(update_data, meme_id)
    update_meme_endpoint.check_status_code(200)

    get_meme_endpoint.get_meme_by_id(meme_id)
    get_meme_endpoint.check_all_fields(update_data)


def test_update_meme_wrong_data(update_meme_endpoint, get_meme_endpoint, meme_id):
    update_data = TEST_DATA_NEGATIVE[1]
    update_data['id'] = meme_id
    update_meme_endpoint.put_meme_by_id(update_data, meme_id)
    update_meme_endpoint.check_status_code(400)


def test_update_nonexistent_meme(update_meme_endpoint):
    update_data = TEST_DATA_UPDATE[0]
    update_data['id'] = 0
    update_meme_endpoint.put_meme_by_id(update_data, 0)
    update_meme_endpoint.check_status_code(404)


def test_delete_meme(delete_meme_endpoint, create_meme_for_delete):
    delete_meme_endpoint.delete_meme_by_id(create_meme_for_delete)
    delete_meme_endpoint.check_status_code(200)


def test_delete_incorrect_meme_id(delete_meme_endpoint):
    delete_meme_endpoint.delete_meme_by_id(0)
    delete_meme_endpoint.check_status_code(404)
