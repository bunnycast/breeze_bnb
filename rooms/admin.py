from django.contrib import admin

from rooms.models import Amenity, Facility, HouseRule, RoomType, Room, Photo


@admin.register(Amenity, Facility, HouseRule, RoomType)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """
    pass
