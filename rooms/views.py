from datetime import datetime
from math import ceil

from django.core.paginator import Paginator
from django.shortcuts import render

from rooms.models import Room


def all_rooms(request):
    page = request.GET.get('page', 1)
    rooms_list = Room.objects.all()
    paginator = Paginator(rooms_list, 10)
    rooms = paginator.get_page(page)
    return render(request, "rooms/home.html", {"rooms": rooms})
