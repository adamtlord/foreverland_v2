from django.core.cache import cache
from django.http import HttpResponse

LOGIN_PATHS = ("/accounts/login/", "/admin/login/")
LOGIN_RATE_LIMIT = 10
LOGIN_RATE_WINDOW = 300


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR") or "unknown"


class LoginRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path in LOGIN_PATHS:
            key = "login-rate:%s" % _client_ip(request)
            count = cache.get(key, 0)
            if count >= LOGIN_RATE_LIMIT:
                return HttpResponse(
                    "Too many login attempts. Try again later.",
                    status=429,
                    content_type="text/plain",
                )
            cache.set(key, count + 1, LOGIN_RATE_WINDOW)
        return self.get_response(request)
