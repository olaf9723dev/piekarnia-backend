from django.conf import settings
from django.urls import path

from dotykackaApi.views import SyncDatabaseViewSet

urlpatterns = [
    path('sync-database/', SyncDatabaseViewSet.as_view({'get': 'get'}), name='sync_database')
]
