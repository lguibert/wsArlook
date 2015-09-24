# -*- coding: utf-8 -*-
import json
from webservice.models import Product, TVA
from django.views.decorators.csrf import csrf_exempt
from general_views import send_response, serialize
from tva_views import get_tva_uuid


def get_products(request):
    products = Product.objects.all()
    return send_response(serialize(products))


def get_product(request, uuid):
    product = Product.objects.get(prod_uuid=uuid)

    tab = {"prod_name": product.prod_name,
           "prod_description": product.prod_description,
           "prod_sellprice": str(product.prod_sellprice),
           "prod_buyprice": str(product.prod_buyprice),
           "prod_datebuy": str(product.prod_datebuy),
           "prod_stock": product.prod_stock,
           "prod_image": product.prod_image,
           "prod_tva_value": str(product.tva.tva_value),
           "prod_lastmodification": str(product.prod_lastmodification),
           }

    return send_response(tab)


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

        product.tva_id = get_tva_uuid(newprod['tva'])

        try:
            product.save()
            print "ah !"
            return send_response(True)
        except:
            print "oh..."
            return send_response(False, 500)
    else:
        return send_response("nothing here for you")
