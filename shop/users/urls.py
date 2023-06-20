from django.urls import path
from . import views
from users.views import (UserLoginView, UserRegisterView)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('register/', UserRegisterView.as_view(), name="register"),
]