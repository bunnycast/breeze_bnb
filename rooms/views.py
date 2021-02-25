from datetime import datetime
from math import ceil

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect

from rooms.models import Room


def all_rooms(request):
    page = request.GET.get('page', 1)
    rooms_list = Room.objects.all()

    paginator = Paginator(rooms_list, 7, orphans=4)
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect('/')



