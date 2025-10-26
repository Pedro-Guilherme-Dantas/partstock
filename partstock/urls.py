from django.contrib import admin
from django.urls import path, include

from .views import part_view, stock_movement_view

urlpatterns = [
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
        'partstock_movementss/<int:pk>/',
        stock_movement_view.StockMovementDetail.as_view(),
        name='detail_stock_movement'
        )
]
