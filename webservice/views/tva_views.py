# -*- coding: utf-8 -*-

from general_views import send_response, serialize
from webservice.models import TVA


def get_tva(request):
    tva = TVA.objects.all()
    return send_response(serialize(tva))


def get_tva_uuid(uuid):
    return TVA.objects.filter(tva_uuid=uuid).values_list('id', flat=True)[0]
