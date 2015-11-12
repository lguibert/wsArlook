# -*- coding: utf-8 -*-
import json
from general_views import send_response, serialize
from webservice.models import Client, LineClient
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


@csrf_exempt
def update_client(request):
    if request.method == 'POST':
        cli = json.loads(request.body)

        client = Client.objects.get(client_uuid=cli['client_uuid'])

        client.client_firstname = cli['client_firstname']
        client.client_lastname = cli['client_lastname']
        client.client_phone = cli['client_phone']
        client.client_address = cli['client_address']
        client.client_town = cli['client_town']
        client.client_zipcode = cli['client_zipcode']
        client.client_email = cli['client_email']

        try:
            client.save()
            return send_response(serialize([client]))
        except:
            return send_response("Problème lors de la mise à jour.", 500)


def line_client(request, uuid):
    cli = Client.objects.get(client_uuid=uuid)
    linescli = LineClient.objects.filter(client_id=cli.id)
    lines = []

    for line in linescli:
        lines.append(
            [line.action.action_name, line.user.username, line.date_modification.strftime("%d/%m/%Y à %H:%M:%S")])

    return send_response(lines)
