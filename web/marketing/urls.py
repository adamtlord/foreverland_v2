from django.urls import path
from marketing import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("video/", views.video, name="video"),
    path("booking/", views.booking, name="booking"),
]
