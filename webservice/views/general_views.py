# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from django.core import serializers
from webservice.models import LineClient, LineProduct


def send_response(data, code=200):
    response = HttpResponse(json.dumps(data), content_type='application/json')
    response.status_code = code
    response["Access-Control-Allow-Origin"] = "*"
    return response


def serialize(data):
    return serializers.serialize('json', data)


# data = {"type": "value", data: {"user":"id","prod":"id" / "client":"id", "action":"id"}}
def trace_action(data):
    if data.type == "prod":
        try:
            lp = LineProduct()
            lp.user = data.data.user
            lp.product = data.data.prod
            lp.action = data.data.action
            lp.save()
            return True
        except:
            return None
    elif data.type == "client":
        try:
            lc = LineClient()
            lc.user = data.data.user
            lc.client = data.data.client
            lc.action = data.data.action
            lc.save()
            return True
        except:
            return None
