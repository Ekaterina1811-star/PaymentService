from django.contrib import admin

from server.apps.payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
