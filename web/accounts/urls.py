from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts.backends.custom import CustomRegistrationView, CustomActivationView
from accounts.forms import RegistrationForm, PasswordResetForm
from accounts.views import login_error, profile_edit, profile_page

urlpatterns = [
    url(
        r"^register/$",
        CustomRegistrationView.as_view(form_class=RegistrationForm),
        name="registration_register",
    ),
    url(
        r"^login/$",
        auth_views.LoginView,
        {"template_name": "registration/login.html"},
        name="auth_login",
    ),
    url(
        r"^login/modal/$",
        auth_views.LoginView,
        {"template_name": "registration/fragments/login_modal.html"},
        name="auth_login_modal",
    ),
    url(r"^login/error/$", login_error, name="login_error"),
    url(r"^logout/$", auth_views.LogoutView, name="auth_logout"),
    url(
        r"^password/reset/$",
        auth_views.PasswordResetView,
        {"password_reset_form": PasswordResetForm},
        name="auth_password_reset",
    ),
    url(
        r"^activate/(?P<activation_key>(?!complete)\w+)/$",
        CustomActivationView.as_view(),
        name="registration_activate",
    ),
    url(r"^profile/(?P<username>[A-Za-z0-9_-]+)$", profile_page, name="profile_page"),
    url(r"^profile/edit/$", profile_edit, name="profile_edit"),
]
