from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Review Admin Definition """

    list_display = ('__str__', 'rating_average',)
