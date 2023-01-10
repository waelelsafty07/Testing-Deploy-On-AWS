from django.urls import path
from .views import usersDetailView, usersView

urlpatterns = [
    path("<int:pk>/", usersDetailView.as_view(), name='user details'),
    path("", usersView.as_view(), name='User'),
]
