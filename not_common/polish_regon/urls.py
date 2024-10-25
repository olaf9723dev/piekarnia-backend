from django.urls import path
from .views import regon_search

urlpatterns = [
    path('search/', regon_search, name='regon_search')
]
