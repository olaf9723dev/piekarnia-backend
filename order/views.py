from django.shortcuts import render, redirect

from core.tools import create_notification
from order.models import OrderDetails, ORDER_STATUS, PAYMENT_STATUS


def admin_orders_list(request):
    orders = OrderDetails.objects.all().order_by('-create_date')

    context = {
        'orders': orders,
        'statuses': ORDER_STATUS
    }

    return render(
        request,
        'orders/orders-list.html',
        context=context
    )


def admin_update_order_status(request, order_id, status):
    order = OrderDetails.objects.get(pk=order_id)
    order.status = status
    order.save()
    return redirect('/order/orders-list/')


def order_details(request, pk):
    order = OrderDetails.objects.get(pk=pk)

    if request.method == 'POST':
        order.status = request.POST.get('order_status')
        order.save()

        create_notification(order.client.user,
                            f'Zmiana statusu zamówienia',
                            f"""Twoje zamówienie o nr {order.order_id} właśnie zmieniło status na: 
                            {ORDER_STATUS[int(order.status) - 1][1]}.""")

    context = {
        'order': order,
        'order_statuses': ORDER_STATUS,
        'payment_statuses': PAYMENT_STATUS
    }

    return render(
        request,
        'orders/order_details.html',
        context=context
    )


def order_delete(request, pk):
    OrderDetails.objects.get(pk=pk).delete()

    return redirect('admin_orders_list')
