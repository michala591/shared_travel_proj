from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    # Add custom fields to the add user form
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": ("user_type", "name", "phone_number", "email"),
            },
        ),
    )

    # Add custom fields to the edit user form
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            None,
            {
                "fields": ("user_type", "name", "phone_number"),
            },
        ),
    )

    # List display options, including is_superuser
    list_display = (
        "username",
        "email",
        "user_type",
        "is_active",
        "is_superuser",
        "is_enabled",
    )
    list_filter = ("user_type", "is_active", "is_superuser")


# Register the custom UserAdmin
admin.site.register(User, UserAdmin)
