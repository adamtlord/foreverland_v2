from django.conf.urls import url
from setter.views import SetterJumpoffView


urlpatterns = [
    url(r"^$", SetterJumpoffView.as_view(template_name='setter/index.html'), name='setter_jumpoff')
]
