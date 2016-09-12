from random import randint

from marketing.models import Testimonial
from apps.common.utils import years_with_gigs


def random_quote(request):
    quote_count = Testimonial.objects.filter(featured=True).count()
    if quote_count:
        random_quote = Testimonial.objects.filter(featured=True)[randint(0, quote_count-1)]
    else:
        random_quote = None
    return {'random_quote': random_quote}


def list_years_with_gigs(request):
    return {'active_years': years_with_gigs}
