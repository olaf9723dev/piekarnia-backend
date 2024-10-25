from django.contrib import admin

from .models import Place, OpeningHours, CustomOpeningHours


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'address', 'zip_code', 'city', 'logo', 'description', 'is_enabled',
                    'enable_date', 'telephone', 'history')


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('place', 'day_of_week', 'start_time', 'end_time', 'history')

@admin.register(CustomOpeningHours)
class CustomOpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('place', 'date', 'start_time', 'end_time', 'is_closed', 'history')
