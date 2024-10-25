from logging import getLogger

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from catalog.forms import ProductInPlaceCreateForm
from catalog.models import ProductInPlace
from .forms import PlaceForm, PlaceCreateForm, PlaceUpdateForm, CustomOpeningHoursForm
from .models import Place, OpeningHours, CustomOpeningHours

LOGGER = getLogger()


class PlacesListView(ListView):
    template_name = 'places/list.html'
    query_set = Place.objects.all().order_by('name')
    # context_object_name = 'places'
    model = Place

    def get_context_data(self, helper=None, **kwargs):
        if self.request.GET.get('token'):
            place_id = self.request.GET.get('state')
            token = self.request.GET.get('token')
            cloud_id = self.request.GET.get('cloudid')
            place = Place.objects.get(pk=place_id)
            place.refresh_token = token
            place.cloud_id = cloud_id
            place.save()

        context = super().get_context_data(**kwargs)
        context.update({
            "dotykacka_url": settings.DOTYKACKA_AUTH_URL,
        })
        return context


def place_detail_view_with_update_opening_hours(request, place_pk):
    try:
        place = Place.objects.get(pk=place_pk)
        place_form = PlaceForm(instance=place)

        products_in_place = ProductInPlace.objects.filter(place_id=place_pk)

        monday, created = OpeningHours.objects.get_or_create(place=place, day_of_week=1)
        tuesday, created = OpeningHours.objects.get_or_create(place=place, day_of_week=2)
        wednesday, created = OpeningHours.objects.get_or_create(place=place, day_of_week=3)
        thursday, created = OpeningHours.objects.get_or_create(place=place, day_of_week=4)
        friday, created = OpeningHours.objects.get_or_create(place=place, day_of_week=5)
        saturday, created = OpeningHours.objects.get_or_create(place=place, day_of_week=6)
        sunday, created = OpeningHours.objects.get_or_create(place=place, day_of_week=7)
        custom_opening_hours = CustomOpeningHours.objects.filter(place__pk=place_pk).order_by('date')

        custom_opening_hours_form = CustomOpeningHoursForm()

        # if monday:
        #     context = {
        #         'place_form': place_form,
        #         'place': place,
        #         'monday': monday,
        #         'tuesday': tuesday,
        #         'wednesday': wednesday,
        #         'thursday': thursday,
        #         'friday': friday,
        #         'saturday': saturday,
        #         'sunday': sunday,
        #         'custom_opening_hours': custom_opening_hours,
        #         'custom_opening_hours_form': custom_opening_hours_form,
        #         'product_in_place_form': product_in_place_form
        #     }
        #     return render(request, 'places/place.html', context)

        if request.method == 'POST':
            custom_opening_hours_form = CustomOpeningHoursForm(request.POST or None)
            if 'opening_hours_update' in request.POST:
                days_in_week = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

                for day in days_in_week:
                    start_request_set = str(
                        request.POST.get(f'{day.day_in_english}_start_time'))
                    end_request_set = str(
                        request.POST.get(f'{day.day_in_english}_end_time'))

                    if start_request_set and end_request_set:
                        if start_request_set == end_request_set:
                            # close the place at that day
                            day.start_time = "00:00"
                            day.end_time = "00:00"
                            day.save()
                        else:
                            day.start_time = request.POST.get(f'{day.day_in_english}_start_time')
                            day.end_time = request.POST.get(f'{day.day_in_english}_end_time')
                            day.save()
                    elif not request.POST.get(f'{day.day_in_english}_start_time') or not request.POST.get(
                            f'{day.day_in_english}_end_time'):
                        pass

                messages.success(request, "Godziny Otwarcia Lokalu zostały zapisane.")

            elif 'custom_opening_hours_form' in request.POST:
                if custom_opening_hours_form.is_valid():
                    new_custom_opening_hours = custom_opening_hours_form.save(commit=False)
                    new_custom_opening_hours.place = place
                    new_custom_opening_hours.save()

                    messages.success(request, "Nowe Niestandardowe Godziny Otwarcia Lokalu zostały utworzone.")

        context = {
            'place_form': place_form,
            'place': place,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'custom_opening_hours': custom_opening_hours,
            'custom_opening_hours_form': custom_opening_hours_form,
            'products_in_place': products_in_place,
            'place_id': place_pk
        }
        return render(request, 'places/place.html', context)

#            days_in_week = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
#            data = custom_opening_hours
#            print(monday)
#            for day in days_in_week:
#                 start_request_set = str(
#                     request.POST.get(f'{day.day_in_english}_start_time'))
#                 end_request_set = str(
#                     request.POST.get(f'{day.day_in_english}_end_time'))
#             for element in change_sources + additional_sources + documentation_sources + various_sources + heating_sources:
#                 data = project.projectsubsidy_set.filter(source=element)
#                 if data.exists():
#                     data = data[0]
#                     element.local_value = data.price_from_community
#                     element.is_enabled = data.is_enabled
#                     element.max_price = data.max_price
#                     element.max_percentage = data.max_percentage
#                     element.max_percentage_total = data.max_percentage_total
#                     element.additional = data.additional
#                     element.description_community = data.description_community
#                     element.only = data.only_with.all()
#
#         structure = generate_project_structure(project_config)
# #
#         return render(request, 'places/place.html', {
#             'project': project,
#             'structure': structure,
#             'clients': Client.objects.all(),
#             'sources': sources
#         })

    except Place.DoesNotExist:
        messages.error(request, "Wybrany lokal nie istnieje.")
        return HttpResponseRedirect(reverse('places/list.html'))


class PlaceCreateView(CreateView):
    model = Place
    form_class = PlaceCreateForm
    template_name = 'places/place_form.html'
    success_url = reverse_lazy('list_of_places')
    permission_required = 'places.create_place'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        place_form = PlaceCreateForm()
        message = 'Utwórz Nowy Lokal'
        context.update({
            "place_form": place_form,
            "message": message
        })
        return context

    def form_valid(self, form):
        place = form.save(commit=False)
        return super(PlaceCreateView, self).form_valid(form)

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane.')
        return super().form_invalid(form)


class PlaceUpdateView(UpdateView):
    model = Place
    form_class = PlaceUpdateForm
    template_name = 'places/place_update_form.html'
    success_url = reverse_lazy('list_of_places')
    # permission_required = 'places.update_place'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        place_form = PlaceUpdateForm(instance=context['object'])
        place = Place.objects.get(pk=self.kwargs['pk'])
        message = f'Aktualizuj Lokal {place.name}'
        context.update({
            "place_form": place_form,
            "message": message
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane podczas aktualizacji lokalizacji.')
        return super().form_invalid(form)


class PlaceDeleteView(DeleteView):
    model = Place
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('list_of_places')
    permission_required = 'places.delete_place'
