import pytest
from rest_framework import status
from django.urls import reverse
from partstock.models import Part
from django.forms.models import model_to_dict

pytestmark = pytest.mark.django_db

def get_post_data(part_factory):
    part_obj = part_factory.build()
    return model_to_dict(part_obj, exclude=['id', 'created_at', 'updated_at'])

@pytest.mark.parametrize('http_method', ['get', 'post', 'patch', 'delete'])
def test_all_operations_denied_unauthenticated(default_client, active_part, http_method, part_factory):
    if http_method in ['post']:
        url = reverse('list_and_create_part')
        data = get_post_data(part_factory)
    else:
        url = reverse('detail_part', kwargs={'pk': active_part.pk})
        data = {'description': 'Attempt to update'}

    client_method = getattr(default_client, http_method)
    response = client_method(url, data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'Authentication credentials were not provided' in response.data['detail']

def test_read_operations_allowed_standard_user(
    auth_client, active_part, part_factory
    ):

    url_list = reverse('list_and_create_part')
    response_list = auth_client.get(url_list)
    assert response_list.status_code == status.HTTP_200_OK

    url_detail = reverse('detail_part', kwargs={'pk': active_part.pk})
    response_detail = auth_client.get(url_detail)
    assert response_detail.status_code == status.HTTP_200_OK

@pytest.mark.parametrize('http_method', ['post', 'patch', 'delete'])
def test_write_operations_denied_standard_user(
    auth_client, active_part, http_method, part_factory
    ):

    if http_method == 'post':
        url = reverse('list_and_create_part')
        data = get_post_data(part_factory)
    else:
        url = reverse('detail_part', kwargs={'pk': active_part.pk})
        data = {'description': 'Attempt to update'}

    client_method = getattr(auth_client, http_method)
    response = client_method(url, data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert 'You do not have permission to perform this action' in response.data['detail']

def test_admin_allowed_full_crud(admin_client, active_part, part_factory):
    url_list = reverse('list_and_create_part')
    data = get_post_data(part_factory)
    response_post = admin_client.post(url_list, data=data)
    assert response_post.status_code == status.HTTP_201_CREATED

    url_detail = reverse('detail_part', kwargs={'pk': active_part.pk})
    response_delete = admin_client.delete(url_detail)
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT