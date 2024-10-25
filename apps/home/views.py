# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from order.models import OrderDetails


@login_required(login_url="/login/")
def index(request):
    total_orders = OrderDetails.objects.all().count()
    new_orders = OrderDetails.objects.filter(status__lt=2).count()
    users_count = User.objects.all().count()
    profits = round(OrderDetails.objects.aggregate(Sum('order_price'))['order_price__sum'], 2)

    context = {
        'total_orders': total_orders,
        'new_orders': new_orders,
        'users_count': users_count,
        'profits': profits
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
