from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django_countries import countries

from rooms.forms import SearchForm
from rooms.models import Room, RoomType, Amenity, Facility, HouseRule


class HomeView(ListView):
    """ HomeView Definition """

    model = Room
    paginate_by = 20
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
    success_url = reverse_lazy("core:home")
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
    success_url = reverse_lazy("core:home")
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


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:

            form = SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # Search Filter Queryset
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__lte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__is_superHost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = Room.objects.filter(**filter_args).order_by("-created_at")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)
                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = SearchForm()
            return render(request, "rooms/search.html", {"form": form})
