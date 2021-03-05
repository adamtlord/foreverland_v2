from django.urls import path
from setter.views import setter_dashboard

urlpatterns = [
    path("", setter_dashboard, {}, name="setter_dashboard"),
]
