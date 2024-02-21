from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.defaults import page_not_found, server_error
from django.views.generic.base import RedirectView
from media.views import behind_the_music, downloads
from shows.views import TheWorksView

admin.autodiscover()

urlpatterns = [
    path("", include("marketing.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("shows/", include("shows.urls")),
    path("songs/", include("songs.urls")),
    path("photos/", include("media.urls")),
    path("fidouche/", include("fidouche.urls")),
    path("setter/", include("setter.urls")),
    path("downloads/", downloads),
    path("behind-the-music/", behind_the_music),
    # Legacy redirects
    path("upcoming-shows/", RedirectView.as_view(url="/shows", permanent=True)),
    path("past-shows/", RedirectView.as_view(url="/shows/past", permanent=True)),
    path("song-list/", RedirectView.as_view(url="/songs", permanent=True)),
    path("news-press/", RedirectView.as_view(url="/", permanent=True)),
    path("quotes/", RedirectView.as_view(url="/about#quotes", permanent=True)),
    path("the-works/", TheWorksView.as_view(), name="the_works"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r"^404/$", page_not_found),
        url(r"^500/$", server_error),
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]
