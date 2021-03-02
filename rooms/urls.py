from django.urls import path

from views import room_detail

app_name = 'rooms'

urlpatterns = [
    path('<int:pk>/', room_detail, name="detail"),
]
