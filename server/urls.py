"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import re_path
from health_check import urls as health_urls
from rest_framework import permissions


from server.apps.main import urls as main_urls
from server.apps.main.views import index

admin.autodiscover()


schema_view = get_schema_view(
   openapi.Info(
      title="Payment Service",
      default_version='v1',
      description="Документация для приложения создания денежных сборов Payment Service",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="admin@payment-service.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Apps:
    path('main/', include(main_urls, namespace='main')),
    path("", include("server.apps.collects.urls")),
    path("", include("server.apps.payment.urls")),
    # Health checks:
    path('health/', include(health_urls)),
    # django-admin:
    path('admin/doc/', include(admindocs_urls)),
    path('admin/', admin.site.urls),
    # Text and xml static files:
    path(
        'robots.txt',
        TemplateView.as_view(
            template_name='common/txt/robots.txt',
            content_type='text/plain',
        ),
        name='robots_txt',
    ),
    path(
        'humans.txt',
        TemplateView.as_view(
            template_name='common/txt/humans.txt',
            content_type='text/plain',
        ),
        name='humans_txt',
    ),
    # It is a good practice to have explicit index view:
    path('', index, name='index'),
    # базовые эндпоинты, для управления пользователями в Django
    path("auth/", include("djoser.urls")),
    # JWT-эндпоинты, для управления JWT-токенами
    path("auth/", include("djoser.urls.jwt")),
]


urlpatterns += [
   re_path(
       r'^swagger(?P<format>\.json|\.yaml)$',
       schema_view.without_ui(cache_timeout=0),
       name='schema-json',
   ),
   re_path(
       r'^swagger/$',
       schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui',
   ),
   re_path(
       r'^redoc/$',
       schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc',
   ),
]


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),
        *urlpatterns,
        # Serving media files in development only:
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
