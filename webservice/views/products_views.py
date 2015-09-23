# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from webservice.models import Product, TVA
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import pprint
import json
import datetime


def get_products(request):
    products = Product.objects.all()
    return send_response(serialize(products))


def get_product(request, uuid):
    product = Product.objects.filter(prod_uuid=uuid)
    return send_response(serialize(product))

@csrf_exempt
def new_product(request):
    if request.method == 'POST':
        newprod = json.loads(request.body)

        product = Product()
        product.prod_name = newprod['name']
        product.prod_description = newprod['description']
        product.prod_sellprice = newprod['sellprice']
        product.prod_buyprice = newprod['buyprice']
        product.prod_datebuy = newprod['datebuy'].split("T")[0]
        product.prod_stock = newprod['stock']
        product.prod_image = newprod['image']
        product.tva_id = 1

        try:
            product.save()
            return send_response(True)
        except:
            return send_response(False, 500)
    else:
        return send_response("nothing here for you")


def send_response(data, code=200):
    response = HttpResponse(json.dumps(data), content_type='application/json')
    response.status_code = code
    response["Access-Control-Allow-Origin"] = "*"
    return response


def serialize(data):
    return serializers.serialize('json', data)
