from django.urls import path

from .views import part_view, stock_movement_view, movement_item_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
        ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
        ),
    path(
        'parts/',
        part_view.ListAndCreatePart.as_view(),
        name='list_and_create_part'
        ),
    path(
        'parts/<int:pk>/',
        part_view.PartDetail.as_view(),
        name='detail_part'
        ),
    path(
        'stock_movements/',
        stock_movement_view.ListAndCreateStockMovement.as_view(),
        name='list_and_create_stock_movement'
        ),
    path(
        'stock_movements/<int:pk>/',
        stock_movement_view.StockMovementDetail.as_view(),
        name='detail_stock_movement'
        ),
    path(
        'movement_items/',
        movement_item_view.ListAndCreateMovementItem.as_view(),
        name='list_and_create_movement_item'
        ),
    path(
        'movement_items/<int:pk>/',
        movement_item_view.MovementItemDetail.as_view(),
        name='detail_movement_items'
        )
]
