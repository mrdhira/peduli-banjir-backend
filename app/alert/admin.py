from django.contrib import admin

# Register your models here.
from .models import Alert


class AlertAdmin(admin.ModelAdmin):
    list_display = (
        "user_report_name",
        "location_address",
        "status",
        "flood_status",
        "flood_depth",
        "is_user_report",
        "is_system_report",
    )

    search_fields = (
        "user_report__full_name",
        "location__address",
    )

    list_filter = (
        "flood_status",
        "flood_depth",
        "is_user_report",
        "is_system_report",
    )

    def user_report_name(self, obj):
        return obj.user_report.full_name

    user_report_name.short_description = "User Report Name"
    user_report_name.admin_order_field = "user_report__full_name"

    def location_address(self, obj):
        return obj.location.address

    location_address.short_description = "Location Address"
    location_address.admin_order_field = "location__address"


admin.site.register(Alert, AlertAdmin)
