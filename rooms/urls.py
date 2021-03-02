from django.urls import path

from views import RoomDetail, EditRoom, CreateRoom

app_name = 'rooms'

urlpatterns = [
    path('create/', CreateRoom.as_view(), name='create'),
    path('<int:pk>/', RoomDetail.as_view(), name="detail"),
    path('<int:pk>/edit/', EditRoom.as_view(), name='edit'),
]
