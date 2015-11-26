# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from django.core import serializers
import decimal


def send_response(data, code=200):
    response = HttpResponse(json.dumps(data, default=decimal_default), content_type='application/json')
    response.status_code = code
    response["Access-Control-Allow-Origin"] = "*"
    return response


def serialize(data):
    return serializers.serialize('json', data)


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError