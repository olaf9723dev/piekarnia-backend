from django.urls import path
from .views import news_list

urlpatterns = [
    path('news', news_list, name='list_of_variant_group'),
    # path('admin/', admin.site.urls),
]
