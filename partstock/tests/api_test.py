from django.forms import model_to_dict
import pytest
from rest_framework import status
from django.urls import reverse
from partstock.models import Part

pytestmark = pytest.mark.django_db

def test_part_list_success(admin_client, part_factory):
    part_factory.create_batch(3)
    url = reverse('list_and_create_part')
    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3

def test_part_create_success(admin_client, part_factory):
    url = reverse('list_and_create_part')
    part_object = part_factory.build(
        name='New Unique Part', 
        current_stock=5,
        cost=10,
        current_price=15
    )

    data = model_to_dict(
        part_object, exclude=['id', 'created_at', 'updated_at']
        )

    response = admin_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'New Unique Part'
    assert response.data['current_stock'] == 0
    assert response.data['cost'] == '10.00'
    assert response.data['current_price'] == '15.00'

def test_part_update_stock_fail(admin_client, active_part):
    url = reverse('detail_part', kwargs={'pk': active_part.pk})

    data = {'current_stock': active_part.current_stock + 10}
    response = admin_client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK

    active_part.refresh_from_db()
    assert active_part.current_stock != data['current_stock']

def test_part_delete_success(admin_client, part_factory):
    unrestricted_part = part_factory()
    url = reverse('detail_part', kwargs={'pk': unrestricted_part.pk})

    response = admin_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Part.objects.filter(pk=unrestricted_part.pk).exists()

def test_part_delete_fail(admin_client, movement_item_factory):
    movement_item = movement_item_factory()
    protected_part = movement_item.part

    url = reverse('detail_part', kwargs={'pk': protected_part.pk})
    response = admin_client.delete(url)

    assert response.status_code in [
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_409_CONFLICT
        ]

    assert Part.objects.filter(pk=protected_part.pk).exists()