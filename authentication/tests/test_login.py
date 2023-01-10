import pytest
endpoint = '/auth'


@pytest.mark.django_db
def test_success_login(client, create_user):
    response = client.post(
        '/auth/login', {"username": create_user.username, "password": "password"})
    print(response.data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_credentials_login(client, create_user):
    response = client.post(
        '/auth/login', {"username": create_user.username, "password": "passwordd"})
    print(response.data)
    assert response.status_code == 400
    assert response.data['non_field_errors'] == [
        'Incorrect Credentials Passed.']


@pytest.mark.django_db
def test_required_fields_login(client, create_user):
    response = client.post(
        '/auth/login')
    print(response.data)
    assert response.status_code == 400
