from authentication.tests.factories import UserFactory
import pytest


@pytest.fixture
def create_user():
    user = UserFactory()
    return user
