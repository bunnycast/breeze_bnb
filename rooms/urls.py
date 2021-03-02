from django.urls import path

from rooms.views import RoomDetail, EditRoom, CreateRoom, SearchView

app_name = "rooms"

urlpatterns = [
    path("create/", CreateRoom.as_view(), name="create"),
    path("<int:pk>/", RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", EditRoom.as_view(), name="edit"),
    path("search/", SearchView.as_view(), name="search"),
]
