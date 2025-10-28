from django.urls import path

from .views.part_view import ListAndCreatePart, PartDetail
from .views.movement_item_view import (
    ListAndCreateMovementItem, MovementItemDetail
)
from .views.stock_movement_view import (
    ListAndCreateStockMovement, StockMovementDetail
)
from .views.sheet_upload_view import PartUpload, TaskDetail
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
        ListAndCreatePart.as_view(),
        name='list_and_create_part'
        ),
    path(
        'parts/<int:pk>/',
        PartDetail.as_view(),
        name='detail_part'
        ),
    path(
        'stock_movements/',
        ListAndCreateStockMovement.as_view(),
        name='list_and_create_stock_movement'
        ),
    path(
        'stock_movements/<int:pk>/',
        StockMovementDetail.as_view(),
        name='detail_stock_movement'
        ),
    path(
        'movement_items/',
        ListAndCreateMovementItem.as_view(),
        name='list_and_create_movement_item'
        ),
    path(
        'movement_items/<int:pk>/',
        MovementItemDetail.as_view(),
        name='detail_movement_items'
        ),
    path(
        'parts/upload/',
        PartUpload.as_view(), name='parts-upload'
        ),
    path(
        'parts/upload/status/<int:pk>/',
        TaskDetail.as_view(), name='task-status'
        ),
]
