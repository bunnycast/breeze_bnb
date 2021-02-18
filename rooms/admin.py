from django.contrib import admin

from rooms.models import Room, RoomType, Amenity, Facility, HouseRule


@admin.register(Amenity, Facility, HouseRule, RoomType, Room)
class RoomAdmin(admin.ModelAdmin):
    pass


# @admin.register(RoomType)
# class RoomTypeAdmin(admin.ModelAdmin):
#     pass
