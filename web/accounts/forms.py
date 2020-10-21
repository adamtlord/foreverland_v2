from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import int_to_base36
from django.template import loader

from registration.forms import RegistrationFormUniqueEmail
from django_common.helper import send_mail_using_template

from accounts.models import UserProfile


class RegistrationForm(RegistrationFormUniqueEmail):
    """Capture other details represented in models.UserProfile and django User class"""
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    RESERVED_USERNAMES = ['admin', 'search', 'uploads', 'static', 'media', 'edit']

    def clean_username(self):
        super(RegistrationForm, self).clean_username()
        username = self.cleaned_data.get('username')
        if username in self.RESERVED_USERNAMES:
            raise forms.ValidationError('This username is already taken.')
        if len(username) < 5:
            raise forms.ValidationError('Usernames should be at least 5 characters long.')
        return username


class UserDetailsForm(forms.ModelForm):
    """Used when users want to edit their details. Hence the multiple excludes below."""
    picture = forms.ImageField(required = False)
    class Meta:
        model = User
        exclude = ('username', 'password', "is_staff", "is_active",
                    "last_login", "date_joined", "is_superuser",
                    "groups", "user_permissions")


class PasswordResetForm(BasePasswordResetForm):

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.pk),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            send_mail_using_template(subject, email_template_name, from_email, [user.email], c, html=True)
