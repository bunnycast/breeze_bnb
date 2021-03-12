from django.urls import path

from lists.views import toggle_room, SeeFavsView

app_name = "lists"

urlpatterns = [
    path("toggle/<int:room_pk>", toggle_room, name="toggle-room"),
    path("favs/", SeeFavsView.as_view(), name="see-favs"),
]
