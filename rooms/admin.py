from django.contrib import admin
from django.utils.safestring import mark_safe

from rooms.models import Amenity, Facility, HouseRule, RoomType, Room, Photo


@admin.register(Amenity, Facility, HouseRule, RoomType)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """
    list_display = ('name', 'used_by',)

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            'Basic Info',
            {'fields': ('name', 'description', 'city', 'country', 'address', 'price',)},
        ),
        (
            'Times',
            {'fields': ('check_in', 'check_out', 'instant_book',)},
        ),
        (
            'Spaces',
            {'fields': ('amenities', 'facilities', 'house_rules',)},
        ),
        (
            'More About the Space',
            {
                'classes': ('collapse',),
                'fields': ('guests', 'beds', 'bedrooms', 'baths',)},
        ),
        (
            'Last Details',
            {'fields': ('host',)}
        ),
    )

    list_display = (
        'id',
        'name',
        'country',
        'city',
        'price',
        'guests',
        'bedrooms',
        'baths',
        'check_in',
        'check_out',
        'instant_book',
        'count_amenities',
        'count_photos',
        'total_rating',
    )

    ordering = ('name', 'price', 'bedrooms',)

    list_filter = (
        'instant_book',
        'host__is_superHost',
        'room_type',
        'amenities',
        'facilities',
        'house_rules',
        'city',
        'country',
    )

    raw_id_fields = ('host',)

    search_fields = ('=city', '^host__username')

    filter_horizontal = (
        'amenities',
        'facilities',
        'house_rules',
    )

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = 'Amenities'

    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = 'Photo Count'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """
    list_display = ('__str__', 'get_thumbnail',)

    def get_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.file.url}" width="50px" />')

    get_thumbnail.short_description = 'Thumbnail'
