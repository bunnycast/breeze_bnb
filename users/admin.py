from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """ Custom User Admin """

    list_display = (
        "username",
        "email",
        "gender",
        "language",
        "currency",
        "is_superHost",
        "email_verified",
        'login_method',
    )
    list_filter = UserAdmin.list_filter + ("is_superHost", 'login_method',)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthday",
                    "language",
                    "currency",
                    "is_superHost",
                    "login_method",
                )
            },
        ),
    )
