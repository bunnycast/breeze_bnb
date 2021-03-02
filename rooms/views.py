from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django_countries import countries

from rooms.models import Room, RoomType, Amenity, Facility, HouseRule


class HomeView(ListView):
    """ HomeView Definition """

    model = Room
    paginate_by = 10
    ordering = "created_at"
    paginate_orphans = 3
    context_object_name = "rooms"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
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


class EditRoom(UpdateView):
    """ Room Edit Definition"""

    model = Room
    template_name = "rooms/room_edit.html"
    success_url = "/"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )


class CreateRoom(CreateView):
    model = Room
    template_name = "rooms/room_create.html"
    success_url = "/"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )


def search(request):
    city = request.GET.get("city", "anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds,", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superHost = bool(request.GET.get("superHost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superHost": superHost,
    }

    room_types = RoomType.objects.all()
    amenities = Amenity.objects.all()
    facilities = Facility.objects.all()
    house_rules = HouseRule.objects.all()

    choices = {
        "room_types": room_types,
        "countries": countries,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }

    # Search Filter Queryset
    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__lte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superHost is True:
        filter_args["host__is_superHost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
