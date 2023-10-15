
from django.urls import include, path
from . import views as view


urlpatterns = [
    path('dashboard/',  view.adminDash, name='admin-dash'),
    path('users/',  view.users, name='admin-users'),
    path('users/details/<int:pk>',  view.userDetails, name='admin-user-details'),
]