from common.utils import years_with_gigs
from marketing.models import Testimonial


def random_quote(request):
    return {
        "random_quote": Testimonial.objects.filter(featured=True).order_by("?").first()
    }


def list_years_with_gigs(request):
    # Eager list so templates do not re-query on every {% for year in active_years %}.
    return {"active_years": years_with_gigs()}
