from django.contrib import admin
from django.urls import include, path


app_name = 'main'


urlpatterns = [
    path("admin/", admin.site.urls),
]


