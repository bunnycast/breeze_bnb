from django.urls import path

from rooms.views import RoomDetail, EditRoomView, CreateRoom, SearchView, RoomPhotosView, delete_photo, EditPhotoView

app_name = "rooms"

urlpatterns = [
    path("create/", CreateRoom.as_view(), name="create"),
    path("<int:pk>/", RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", RoomPhotosView.as_view(), name="photos"),
    path("<int:room_pk>/photos/<int:photo_pk>/delete/", delete_photo, name="delete-photo"),
    path("<int:room_pk>/photos/<int:photo_pk>/edit/", EditPhotoView.as_view(), name="edit-photo"),
    path("search/", SearchView.as_view(), name="search"),
]
