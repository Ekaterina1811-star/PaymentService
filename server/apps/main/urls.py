from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("collects.urls")),
    path("", include("payments.urls")),
    path("", include("users.urls")),
]

# Зарегать пользователя http://127.0.0.1:8000/auth/users/
# http://127.0.0.1:8000/auth/jwt/create/ получаем токен
# создаем повод
# http://127.0.0.1:8000/occasion/


