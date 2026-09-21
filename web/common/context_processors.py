import random

from django.conf import settings
from django.core.cache import cache

from common.utils import years_with_gigs
from marketing.models import Testimonial


def random_quote(request):
    quote = cache.get("featured_quote")
    if quote is None:
        featured = list(Testimonial.objects.filter(featured=True)[:20])
        if featured:
            quote = random.choice(featured)
            cache.set("featured_quote", quote, 60 * 5)
        else:
            quote = None
    return {"random_quote": quote or None}


def list_years_with_gigs(request):
    return {"active_years": years_with_gigs()}


def social_links(request):
    return {
        "FACEBOOK_PAGE_URL": settings.FACEBOOK_PAGE_URL,
        "FACEBOOK_APP_ID": settings.FACEBOOK_APP_ID,
        "FACEBOOK_SDK_VERSION": settings.FACEBOOK_SDK_VERSION,
        "INSTAGRAM_PROFILE_URL": settings.INSTAGRAM_PROFILE_URL,
    }
