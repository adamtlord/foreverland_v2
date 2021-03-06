import urllib

import simplejson
from django.conf import settings
from django.utils.encoding import smart_str


def get_lat_lng(location):
    location = urllib.parse.quote_plus(smart_str(location))
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&sensor=false&key={settings.GOOGLE_MAPS_API_KEY}"

    response = urllib.request.urlopen(url).read()
    result = simplejson.loads(response)
    if result["status"] == "OK":
        lat = str(result["results"][0]["geometry"]["location"]["lat"])
        lng = str(result["results"][0]["geometry"]["location"]["lng"])
        return "%s,%s" % (lat, lng)
    else:
        return ""


def years_with_gigs():
    from shows.models import Show

    years = []
    years_with_gigs = Show.objects.all().dates("date", "year")
    for year in years_with_gigs:
        years.append(year.year)
    return years
