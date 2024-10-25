from django.urls import path
from .views import PlacesListView, PlaceUpdateView, PlaceDeleteView, PlaceCreateView, \
    place_detail_view_with_update_opening_hours

urlpatterns = [
    path('list', PlacesListView.as_view(), name='list_of_places'),
    path('list/<int:place_pk>/details', place_detail_view_with_update_opening_hours, name='place'),
    path('list/create', PlaceCreateView.as_view(), name='place_create'),
    path('list/<int:pk>/details/update', PlaceUpdateView.as_view(), name='place_update'),
    path('list/<int:pk>/details/delete', PlaceDeleteView.as_view(), name='place_delete'),
]
