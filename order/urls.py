from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('orders-list/', views.admin_orders_list, name='admin_orders_list'),
    path('orders-details/<int:pk>/', views.order_details, name='admin_order_details'),
    path('orders-delete/<int:pk>/', views.order_delete, name='admin_order_delete'),
    path('orders-delete/<int:order_id>/update-status/<int:status>', views.admin_update_order_status, name='admin_update_status'),
]
