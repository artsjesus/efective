from django.contrib import admin
from orders.models import Order


@admin.register(Order)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("table_number", "items", "status", "total_price")
