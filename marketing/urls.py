from django.conf.urls import url
from marketing import views

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^about/$', views.about),
    url(r'^faq/$', views.faq),
    url(r'^video/$', views.video),
    url(r'^booking/$', views.booking),
]
