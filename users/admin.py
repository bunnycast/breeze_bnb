from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    """ Custom User Admin """
    list_display = ['username', "email", 'gender', 'language', 'currency', 'is_superHost']
    list_filter = ('language', 'currency', 'is_superHost',)
