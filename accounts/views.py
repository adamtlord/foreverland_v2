from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts.forms import UserDetailsForm


def profile_page(request, username, template='accounts/profile_page.html'):
    d = {}
    d['this_user'] = get_object_or_404(User, username=username)
    return render(request, template, d)


@login_required
def profile_edit(request,  template='accounts/profile_edit.html'):
    d = {}
    if request.method == 'GET':
        form = UserDetailsForm(instance = request.user)
    else:
        form = UserDetailsForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            user = form.save()
            profile = user.get_profile()
            profile.save()
            user.save()
            messages.add_message(request, messages.SUCCESS,
                'Your account has been updated')
            return redirect(reverse('profile_edit'))


    d['form'] = form
    return render(request, template, d)


def login_error(request, template='accounts/login_error.html'):
    d = {}
    return render(request, template, d)
