from django.shortcuts import render


def login_error(request, template="accounts/login_error.html"):
    d = {}
    return render(request, template, d)
