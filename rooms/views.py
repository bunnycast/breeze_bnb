from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView

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


class RoomDetail(DetailView):
    """ Room Detail Definition"""
    model = Room

# # FBV
# def room_detail(request, pk):
#     try:
#         room = Room.objects.get(pk=pk)
#         return render(request, 'rooms/detail.html', {'room':room})
#     except Room.DoesNotExist:
#         raise Http404()
