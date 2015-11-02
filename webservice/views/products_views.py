# -*- coding: utf-8 -*-
import json
from webservice.models import Product
from django.views.decorators.csrf import csrf_exempt
from general_views import send_response, serialize
from tva_views import get_tva_uuid


def get_products(request):
    products = Product.objects.all()
    return send_response(serialize(products))


@csrf_exempt
def new_product(request):
    if request.method == 'POST':
        newprod = json.loads(request.body)

        product = Product()
        product.prod_name = newprod['name']
        product.prod_sellprice = newprod['sellprice']
        product.prod_buyprice = newprod['buyprice']
        product.prod_datebuy = newprod['datebuy'].split("T")[0]
        product.prod_stock = newprod['stock']
        product.prod_image = newprod['image']

        product.tva_id = get_tva_uuid(newprod['tva'])

        try:
            product.save()
            return send_response(True)
        except:
            return send_response(False, 500)


@csrf_exempt
def in_product(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if update_product(data[0], data[1], "+"):
            return send_response(True)
        else:
            return send_response("Erreur lors de la mise à jour du produit.", 500)


@csrf_exempt
def out_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if update_product(data[0], data[1], "-"):
            return send_response(True)
        else:
            return send_response("Erreur lors de la mise à jour du produit.", 500)


def update_product(uuid, quantity, operation):
    try:
        prod = Product.objects.get(prod_uuid=uuid)
        if operation == "+":
            prod.prod_stock = int(prod.prod_stock) + int(quantity)
        elif operation == "-":
            prod.prod_stock = int(prod.prod_stock) - int(quantity)

        prod.save()
        return True
    except:
        return False
