from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("htmx/", views.UsersHTMxTableView.as_view(), name="users_htmx"),
]
