from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView, FormView, View

from rooms.forms import SearchForm, CreatePhotoForm, CreateRoomForm
from rooms.models import Room, RoomType, Amenity, Facility, HouseRule, Photo
from users import mixins


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


class EditRoomView(mixins.LoggedInOnlyView, UpdateView):
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

    # 내가 host가 아닌 방은 수정 못함
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(mixins.LoggedInOnlyView, DetailView):
    model = Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "can't delete that photo")
        else:
            Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted!")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated!"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):
    model = Photo
    template_name = "rooms/photo_create.html"
    fields = (
        "caption",
        "file",
    )
    form_class = CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Upload")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(mixins.LoggedInOnlyView, FormView):
    form_class = CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save(self.request.user)
        room.host = self.request.user
        room.save()
        # many to many field save method
        form.save_m2m()
        messages.success(self.request, "Room Created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


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
