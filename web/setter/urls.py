from django.urls import path
from setter.views import setter_dashboard, view_setlist

urlpatterns = [
    path("", setter_dashboard, {}, name="setter_dashboard"),
    path("setlist/<int:gig_id>", view_setlist, {}, name="view_setlist")
]
