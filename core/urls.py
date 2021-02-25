from django.urls import path, include
from rooms import views as rooms_views

app_name = "core"

urlpatterns = [
    path("", rooms_views.all_rooms, name=""),
]