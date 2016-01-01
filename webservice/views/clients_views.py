# -*- coding: utf-8 -*-
import json
from general_views import send_response, serialize
from webservice.models import Client, LineClient, Visit, User
from django.views.decorators.csrf import csrf_exempt

date_format = "%d/%m/%Y"


def get_clients(request):
    clients = Client.objects.filter(active=1)
    clis = []
    for client in clients:
        visit = Visit.objects.filter(client_id=client.id).order_by("-visit_date")[:1]
        if visit:
            client.client_visit = visit[0].visit_date.strftime(date_format)
        else:
            client.client_visit = "Aucune visite"

        c = {"client_firstname": client.client_firstname,
             "client_lastname": client.client_lastname,
             "client_phone": client.client_phone,
             "client_address": client.client_address,
             "client_town": client.client_town,
             "client_zipcode": client.client_zipcode,
             "client_email": client.client_email,
             "client_uuid": str(client.client_uuid),
             "client_visit": client.client_visit
             }

        clis.append(c)

    return send_response(clis)


def get_client(request, uuid):
    client = Client.objects.get(client_uuid=uuid)
    visit = Visit.objects.filter(client_id=client.id)

    visits = []
    for v in visit:
        visits.append(v.visit_date.strftime(date_format))

    client = {"client_firstname": client.client_firstname,
              "client_lastname": client.client_lastname,
              "client_phone": client.client_phone,
              "client_address": client.client_address,
              "client_town": client.client_town,
              "client_zipcode": client.client_zipcode,
              "client_email": client.client_email,
              "client_uuid": str(client.client_uuid),
              "client_visit": visits
              }

    return send_response(client)


@csrf_exempt
def new_client(request):
    if request.method == 'POST':
        newclient = json.loads(request.body)

        client = Client()
        client.client_firstname = newclient['firstname']
        client.client_lastname = newclient['lastname']
        try:
            client.client_phone = newclient['phone']
            client.client_address = newclient['address']
            client.client_town = newclient['town']
            client.client_zipcode = newclient['zipcode']
            client.client_email = newclient['email']
        except:
            pass

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
            [line.action.action_name, line.user.username, line.date_modification])

    return send_response(lines)


@csrf_exempt
def update_visit_client(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uuid = data[0]
        value = data[1]
        username = data[2]
        try:
            client = Client.objects.get(client_uuid=uuid)
            v = Visit()
            v.client = client
            v.value = value
            v.user = User.objects.get(username=username)
            v.save()
            return send_response(True)
        except:
            return send_response("Erreur lors de la sauvegarde la nouvelle visite.", 500)
