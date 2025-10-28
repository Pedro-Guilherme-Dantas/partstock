import pytest
from factory import fuzzy
from factory.django import DjangoModelFactory
from partstock.models import Part, StockMovement, MovementItem
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from factory import SubFactory, LazyAttribute
from django.contrib.auth import get_user_model
import factory.fuzzy

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.fuzzy.FuzzyText(length=10)
    email = factory.LazyAttribute(lambda o: f'{o.username}@test.com')
    is_active = True


class PartFactory(DjangoModelFactory):
    class Meta:
        model = Part

    name = fuzzy.FuzzyText(length=12, prefix='Part_')
    description = "Description"
    cost = fuzzy.FuzzyDecimal(1.00, 50.00, 2)
    current_price = fuzzy.FuzzyDecimal(50.00, 100.00, 2)
    current_stock = fuzzy.FuzzyInteger(1, 20)
    is_active = True


class StockMovementFactory(DjangoModelFactory):
    class Meta:
        model = StockMovement

    movement_type = 'IN'
    date_recorded = timezone.now()
    notes = fuzzy.FuzzyText(length=50)


class MovementItemFactory(DjangoModelFactory):
    class Meta:
        model = MovementItem

    part = SubFactory(PartFactory)
    movement = SubFactory(StockMovementFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 10)
    unit_price_at_transaction = LazyAttribute(
        lambda obj: obj.part.current_price
        )
    unit_cost_at_transaction = LazyAttribute(lambda obj: obj.part.cost)

def get_auth_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client

@pytest.fixture
def user_factory():
    return UserFactory

@pytest.fixture
def part_factory():
    return PartFactory

@pytest.fixture
def stock_movement_factory():
    return StockMovementFactory

@pytest.fixture
def movement_item_factory():
    return MovementItemFactory

@pytest.fixture
def active_part(part_factory):
    return part_factory()

@pytest.fixture
def test_user(user_factory):
    return user_factory(is_staff=False, is_superuser=False)

@pytest.fixture
def admin_user(user_factory):
    return user_factory(is_staff=True, is_superuser=True)

@pytest.fixture
def auth_client(test_user):
    return get_auth_client(test_user)

@pytest.fixture
def admin_client(admin_user):
    return get_auth_client(admin_user)

@pytest.fixture
def default_client():
    return APIClient()

@pytest.fixture
def api_client():
    return APIClient()