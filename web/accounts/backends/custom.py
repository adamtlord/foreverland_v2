from django.contrib.auth import authenticate, login
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.requests import RequestSite
from django.contrib.sites.models import Site

from registration.backends.default.views import RegistrationView, ActivationView
from registration.models import RegistrationProfile
from registration.signals import user_activated
from django_common.helper import send_mail_using_template

from accounts.models import UserProfile


class CustomRegistrationView(RegistrationView):
    """A custom registration view that saves extra User's details"""
    def register(self, request, **cleaned_data):
        """Register the new user."""
        # Create user and store the first/last name.
        new_user = super(CustomRegistrationView, self).register(
            request, **cleaned_data)
        new_user.first_name = cleaned_data['first_name']
        new_user.last_name = cleaned_data['last_name']
        new_user.save()

        # Store the common profile data.
        UserProfile.objects.create(user=new_user)

        # NOTE: activate and log in user according to settings
        if getattr(settings, 'AUTOMATIC_ACTIVATION_AFTER_REGISTRATION', True):
            registration_profile = new_user.registrationprofile_set.order_by('-id')[0]
            CustomActivationView().activate(request, registration_profile.activation_key)

            # Login this user.
            authenticated_user = authenticate(username=cleaned_data['username'],
                password=cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)

        return new_user


class CustomActivationView(ActivationView):

    def activate(self, request, activation_key):
        activated_user = RegistrationProfile.objects.activate_user(activation_key)
        if activated_user:
            user_activated.send(sender='activate_user',
                                user=activated_user,
                                request=request)

            if getattr(settings, 'SEND_EMAIL_AFTER_ACTIVATION', False):
                if Site._meta.installed:
                    site = Site.objects.get_current()
                else:
                    site = RequestSite(request)
                ctx_dict = {'user': activated_user, 'site': site}
                subject = render_to_string('registration/postactivation_email_subject.txt', ctx_dict)
                subject = ''.join(subject.splitlines())
                send_mail_using_template(subject, 'registration/postactivation_email.html', settings.DEFAULT_FROM_EMAIL, [activated_user.email], ctx_dict, html=True)
        return activated_user


def send_activation_email(self, site):
    if getattr(settings, 'SEND_EMAIL_AFTER_REGISTRATION', False):
        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site}
        subject = render_to_string('registration/activation_email_subject.txt', ctx_dict)
        subject = ''.join(subject.splitlines())
        send_mail_using_template(subject, 'registration/activation_email.html', settings.DEFAULT_FROM_EMAIL, [self.user.email], ctx_dict, html=True)

RegistrationProfile.send_activation_email = send_activation_email
