# -*- coding: utf-8 -*-
import json
from general_views import send_response, serialize
from webservice.models import Client
from django.views.decorators.csrf import csrf_exempt


def get_clients(request):
    clients = Client.objects.filter(active=1)
    return send_response(serialize(clients))


def get_client(request, uuid):
    client = Client.objects.filter(client_uuid=uuid)
    return send_response(serialize(client))


@csrf_exempt
def new_client(request):
    if request.method == 'POST':
        newclient = json.loads(request.body)

        client = Client()
        client.client_firstname = newclient['firstname']
        client.client_lastname = newclient['lastname']
        client.client_phone = newclient['phone']
        client.client_address = newclient['address']
        client.client_town = newclient['town']
        client.client_zipcode = newclient['zipcode']
        client.client_email = newclient['email']

        try:
            client.save()
            return send_response(True)
        except:
            return send_response(False, 500)
    else:
        return send_response("nothing here for you")
