import json
from django.shortcuts import HttpResponse
from django.conf import settings
from not_common.polish_regon.service import RegonService



def regon_search(request):
    sandbox = True
    api_key = None
    try:
        sandbox = settings.REGON_USE_SANDBOX
        api_key = settings.REGON_API_KEY
    except:
        pass
    regon_service = RegonService(sandbox=sandbox, api_key=api_key)
    search_kwargs = {}
    if request.GET.get('nip'):
        search_kwargs['nip'] = request.GET['nip']
    return HttpResponse(json.dumps(regon_service.search(**search_kwargs)), content_type='application/json')
