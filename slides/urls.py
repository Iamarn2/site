import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
import slides.blog.views
from .api import api_router


#path('comments/', include('django_comments_xtd.urls')),
#path('comment/', include('django_comments.urls')),

# ccылка для комментариев webapp
#    path('comments/', include('slides.custom_comments.urls')),
#    path('comment/', include('django_comments.urls')),
#    path('accounts/', include('allauth.urls')),
#    path('accounts/', include('slides.userauth.urls')),
#   prefix_default_language=False,
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("sitemap.xml", sitemap),
    path("api/v2/", api_router.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path('robots.txt', slides.blog.views.RobotsView.as_view()),
    path("", include(wagtail_urls)),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('slides.userauth.urls')),
    path('comments/', include('slides.custom_comments.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView
    from django.views.generic.base import RedirectView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path(
            "favicon.ico",
            RedirectView.as_view(url=settings.STATIC_URL + "img/bread-favicon.ico"),
        )
    ]

    # Add views for testing 404 and 500 templates
    #    path("test404/", TemplateView.as_view(template_name="404.html")),
    #    path("test500/", TemplateView.as_view(template_name="500.html")),
    urlpatterns += [
        path('404/', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        path('500/', default_views.server_error),
    ]
