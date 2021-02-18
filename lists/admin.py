from django.contrib import admin

from lists.models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    """ List Admin Definition """
    pass
