import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings
from django.utils.encoding import smart_str

logger = logging.getLogger(__name__)


def get_lat_lng(location):
    location = urllib.parse.quote_plus(smart_str(location))
    key = settings.GOOGLE_MAPS_API_KEY or ""
    if not key:
        return ""
    url = (
        "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s"
        % (location, key)
    )
    try:
        response = urllib.request.urlopen(url, timeout=5).read()
        result = json.loads(response)
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        logger.warning("Geocoding failed for %s: %s", location, exc)
        return ""
    if result.get("status") == "OK":
        lat = str(result["results"][0]["geometry"]["location"]["lat"])
        lng = str(result["results"][0]["geometry"]["location"]["lng"])
        return "%s,%s" % (lat, lng)
    return ""


def years_with_gigs():
    from django.core.cache import cache
    from shows.models import Show

    cached = cache.get("years_with_gigs")
    if cached is not None:
        return cached
    years = [dt.year for dt in Show.objects.dates("date", "year")]
    if years:
        cache.set("years_with_gigs", years, 60 * 60 * 24)
    return years
