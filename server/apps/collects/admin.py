from django.contrib import admin

from server.apps.collects.models import Collect, Occasion


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    pass


@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    pass
