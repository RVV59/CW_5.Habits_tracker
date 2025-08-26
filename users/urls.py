from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .apps import UsersConfig
from .views import UserCreateAPIView, UserListAPIView, UserRetrieveUpdateDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('login/', obtain_auth_token, name='user_login'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_detail'),
]