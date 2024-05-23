from django.urls import path
from .views import RegisterUserApi, user_info

urlpatterns = [
    path('register/', RegisterUserApi.as_view()),
    path('user_info/', user_info)
]
