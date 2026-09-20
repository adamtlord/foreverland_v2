from django.conf import settings

from common.utils import years_with_gigs
from marketing.models import Testimonial


def random_quote(request):
    return {
        "random_quote": Testimonial.objects.filter(featured=True).order_by("?").first()
    }


def list_years_with_gigs(request):
    # Eager list so templates do not re-query on every {% for year in active_years %}.
    return {"active_years": years_with_gigs()}


def social_links(request):
    return {
        "FACEBOOK_PAGE_URL": settings.FACEBOOK_PAGE_URL,
        "FACEBOOK_APP_ID": settings.FACEBOOK_APP_ID,
        "FACEBOOK_SDK_VERSION": settings.FACEBOOK_SDK_VERSION,
        "INSTAGRAM_PROFILE_URL": settings.INSTAGRAM_PROFILE_URL,
    }
