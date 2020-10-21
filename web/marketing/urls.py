from django.conf.urls import url
from marketing import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^video/$', views.video, name='video'),
    url(r'^booking/$', views.booking, name='booking'),
]
