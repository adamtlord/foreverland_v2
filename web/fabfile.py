from django.conf import settings

from fabric.api import local


def rs():
    """
    Shortcut to do quick runserver
    """
    if "gunicorn" in settings.INSTALLED_APPS:
        try:
            local("kill -TERM `cat gunicorn.pid`")
        except Exception:
            print("No existing gunicorn process")
        local("python manage.py run_gunicorn -w 4 --timeout=240 --pid=gunicorn.pid")
    else:
        local("python manage.py runserver 0.0.0.0:8000")
