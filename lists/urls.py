from django.urls import path

from lists.views import save_room

app_name = "lists"

urlpatterns = [
    path("add/<int:room_pk>", save_room, name="save-room"),
]
