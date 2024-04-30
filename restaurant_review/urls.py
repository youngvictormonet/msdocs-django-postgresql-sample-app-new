from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("htmx/", views.UsersHTMxTableView.as_view(), name="users_htmx"),
    path('<int:id>/', views.details, name='details'),
    path('create', views.create_restaurant, name='create_restaurant'),
    path('add', views.add_restaurant, name='add_restaurant'),
    path('review/<int:id>', views.add_review, name='add_review'),
]
