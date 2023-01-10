import pytest
from knox.auth import AuthToken
from rest_framework.test import APIClient


@pytest.fixture
def auth_client(create_user):
    _, token = AuthToken.objects.create(create_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    return client, create_user.id


pytest_plugins = [
    "authentication.tests.fixtures",
]
