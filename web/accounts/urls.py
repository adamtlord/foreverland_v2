from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import login_error

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="auth_login",
    ),
    path("login/error/", login_error, name="login_error"),
    path("logout/", auth_views.LogoutView.as_view(), name="auth_logout"),
]
