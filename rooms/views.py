from datetime import datetime
from math import ceil

from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from rooms.models import Room


class HomeView(ListView):
    """ HomeView Definition """

    model = Room
    paginate_by = 10
    ordering = 'created_at'
    paginate_orphans = 3
    context_object_name = 'rooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['now'] = now
        return context


def room_detail(request, pk):
    try:
        room = Room.objects.get(pk=pk)
        return render(request, 'rooms/detail.html', {'room':room})
    except Room.DoesNotExist:
        raise Http404()
