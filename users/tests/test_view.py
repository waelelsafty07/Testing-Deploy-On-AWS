import pytest
from knox.auth import AuthToken
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_all_user(client, create_user):
    response = client.get('/users/')
    assert response.status_code == 200
    assert len(response.data['users']) != 0


@pytest.mark.django_db
def test_not_found_user(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert len(response.data['users']) == 0


@pytest.mark.django_db
def test_get_authorized_without_token_user(client):
    response = client.get('/users/1/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_authorized_with_token_user(auth_client):
    client, create_user = auth_client
    response = client.get(f'/users/{create_user}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_unauthorized_with_token_user(auth_client):
    client, create_user = auth_client
    response = client.get(f'/users/{create_user+1}/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_put_unauthorized_with_token_user(auth_client):
    client, create_user = auth_client
    response = client.put(f'/users/{create_user+1}/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_put_unauthorized_without_token_user(client):
    response = client.put(f'/users/{1}/', {"username": "ksdsdsd"})
    assert response.status_code == 401


@pytest.mark.django_db
def test_put_authorized_with_token_user(auth_client):
    client, create_user = auth_client
    response = client.put(f'/users/{create_user}/', {"username": "ksds"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_patch_deactivate_authorized_with_token_user(auth_client):
    client, create_user = auth_client
    response = client.patch(f'/users/{create_user}/')
    assert response.status_code == 200
    assert response.data['message'] == "Account will be deleted in  29 days, and you can't retreive it again \n\tYou can login again to active your account in 29 days"


@pytest.mark.django_db
def test_patch_deactivate_unauthorized_without_token_user(client):
    response = client.patch(f'/users/1/')
    assert response.status_code == 401
    print(response.data)
    assert response.data['detail'] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_patch_deactivate_unauthorized_with_token_user(auth_client):
    client, create_user = auth_client
    response = client.patch(f'/users/{create_user+1}/')
    assert response.status_code == 401
    print(response.data)
    assert response.data['message'] == "unauthorized"
