from django.contrib import admin

from rooms.models import Room, RoomType


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    pass
