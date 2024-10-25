import json

from django.http import HttpResponse
from django.shortcuts import render

from cms.models import News
from cms.serializers import NewsSerializer


def news_list(request):
    return HttpResponse(json.dumps([{"title": x.title, "content": x.content} for x in News.objects.all()]),
                        content_type='application/json')
