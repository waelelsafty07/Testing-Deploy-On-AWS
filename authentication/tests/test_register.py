from .factories import UserFactory
import pytest
from users.models import Users
endpoint = '/auth'


@pytest.fixture
def body():
    body = {
        "username": "exampleUsername",
        "email": "exampleUsername@gmail.com",
        "password": "exampleUsername",
        "passwordConfirm": "exampleUsername"
    }
    return body


@pytest.mark.django_db
def test_success_register(client, body):
    expectedResponse = {'username': 'exampleUsername',
                        'email': 'exampleUsername@gmail.com'}
    response = client.post(f'{endpoint}/register', body)
    assert response.status_code == 201
    # assert response.data == expectedResponse


@pytest.mark.django_db
def test_exist_user_register(client, create_user, body):
    body['username'] = create_user.username
    body['email'] = create_user.email
    expectedResponse = {
        "username": [
            "This field must be unique."
        ],
        "email": [
            "This field must be unique."
        ]
    }

    response = client.post(f'{endpoint}/register', body)

    assert response.status_code == 400
    assert response.data == expectedResponse


@pytest.mark.django_db
def test_Data_required_register(client):
    body = dict()
    expectedResponse = {
        "username": [
            "This field is required."
        ],
        "email": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ],
        "passwordConfirm": [
            "This field is required."
        ]
    }
    response = client.post(f'{endpoint}/register', body)
    assert response.status_code == 400
    assert response.data == expectedResponse


@pytest.mark.django_db
def test_Data_blank_register(client, body):
    body["username"] = ""
    expectedResponse = {
        "username": [
            "This field may not be blank."
        ]
    }
    response = client.post(f'{endpoint}/register', body)
    assert response.status_code == 400
    assert response.data["username"] == expectedResponse["username"]


@pytest.mark.django_db
def test_email_not_correct_register(client, body):
    body["email"] = "emai"
    expectedResponse = {"email": ["Enter a valid email address."]}
    response = client.post(f'{endpoint}/register', body)
    assert response.status_code == 400
    assert response.data == expectedResponse


@pytest.mark.django_db
def test_password_less_than_8_register(client, body):
    body["password"] = "less8"
    body["passwordConfirm"] = "less8"
    expectedResponse = {"password": [
        "This password is too short. It must contain at least 8 characters."
    ],
        "passwordConfirm": [
        "This password is too short. It must contain at least 8 characters."
    ]
    }
    response = client.post(f'{endpoint}/register', body)
    assert response.status_code == 400
    assert response.data == expectedResponse
