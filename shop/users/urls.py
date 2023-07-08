from django.urls import path, include
from users.views import profile
from users.views import logout_view
from django.contrib.auth import views as auth_views

from users.views import UserLoginView, UserRegisterView, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView, EmailConfirmationFailedView


urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout', logout_view, name='logout'),
    path('register/', UserRegisterView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(),
         name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/',
         UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(),
         name='email_confirmation_failed'),
]
