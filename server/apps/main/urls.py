from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path


schema_view = get_schema_view(
   openapi.Info(
      title="Payment Service",
      default_version='v1',
      description="Документация для приложения создания денежных сборов Payment Service",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="admin@kittygram.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("collects.urls")),
    path("", include("payments.urls")),
    path("", include("users.urls")),
    # базовые эндпоинты, для управления пользователями в Django
    path("auth/", include("djoser.urls")),
    # JWT-эндпоинты, для управления JWT-токенами
    path("auth/", include("djoser.urls.jwt")),
]

# Зарегать пользователя http://127.0.0.1:8000/auth/users/
# http://127.0.0.1:8000/auth/jwt/create/ получаем токен
# создаем повод
# http://127.0.0.1:8000/occasion/

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$',
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
