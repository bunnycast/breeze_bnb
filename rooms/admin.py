from django.contrib import admin

from rooms.models import Amenity, Facility, HouseRule, RoomType, Room, Photo


@admin.register(Amenity, Facility, HouseRule, RoomType)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """
    list_display = ('name', 'used_by',)

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

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


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """
    pass
