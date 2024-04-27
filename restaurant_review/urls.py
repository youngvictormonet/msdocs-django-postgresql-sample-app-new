from django.urls import path

from . import views

from app import forms, views

from app.views import (
    UsersHTMxTableView
)

urlpatterns = [
    path('', views.home, name='home'),
    path("htmx/", UsersHTMxTableView.as_view(), name="users_htmx"),
    path('<int:id>/', views.details, name='details'),
    path('create', views.create_restaurant, name='create_restaurant'),
    path('add', views.add_restaurant, name='add_restaurant'),
    path('review/<int:id>', views.add_review, name='add_review'),
]
