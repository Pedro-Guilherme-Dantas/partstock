from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('parts/', views.ListAndCreatePart.as_view(), name='list_and_create_part'),
    path('parts/<int:pk>/', views.PartDetail.as_view(), name='detail_part')
]
