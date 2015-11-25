# -*- coding: utf-8 -*-
import json
from webservice.models import Product, LineProduct, Sell, User, TVA
from django.views.decorators.csrf import csrf_exempt
from general_views import send_response, serialize
from tva_views import get_tva_uuid
import datetime


def get_products(request):
    products = Product.objects.filter(active=1)
    return send_response(serialize(products))


def get_product(request, uuid):
    product = Product.objects.get(prod_uuid=uuid)

    tab = {"prod_name": product.prod_name,
           "prod_sellprice": str(product.prod_sellprice),
           "prod_buyprice": str(product.prod_buyprice),
           "prod_datebuy": product.prod_datebuy.strftime("%m/%d/%Y"),
           "prod_stock": product.prod_stock,
           "prod_stock_store": product.prod_stock_store,
           "prod_image": product.prod_image,
           "prod_tva_value": str(product.tva.tva_value),
           "prod_uuid": str(product.prod_uuid),
           "prod_tva": str(product.tva.tva_uuid)
           }

    return send_response(tab)


@csrf_exempt
def new_product(request):
    if request.method == 'POST':
        newprod = json.loads(request.body)

        try:
            if not newprod['image']:
                newprod['image'] = None
        except:
            newprod['image'] = None

        product = Product()
        product.prod_name = newprod['name']
        product.prod_sellprice = newprod['sellprice']
        product.prod_buyprice = newprod['buyprice']
        product.prod_datebuy = newprod['datebuy'].split("T")[0]
        product.prod_stock = newprod['stock']
        product.prod_stock_store = newprod['stock_store']
        product.prod_image = newprod['image']

        product.tva_id = get_tva_uuid(newprod['tva'])

        try:
            product.save()
            return send_response(True)
        except:
            return send_response(False, 500)


@csrf_exempt
def update_product(request):
    if request.method == 'POST':
        prod = json.loads(request.body)

        product = Product.objects.get(prod_uuid=prod['prod_uuid'])

        product.prod_name = prod['prod_name']
        product.prod_sellprice = prod['prod_sellprice']
        product.prod_buyprice = prod['prod_buyprice']
        product.prod_datebuy = prod['prod_datebuy']
        product.prod_stock = prod['prod_stock']
        product.prod_stock_store = prod['prod_stock_store']
        product.prod_image = prod['prod_image']

        product.tva_id = get_tva_uuid(prod['prod_tva'])

        try:
            product.save()

            splited = product.prod_datebuy.split("-")
            product.prod_datebuy = datetime.date(int(splited[0]), int(splited[1]), int(splited[2]))

            return send_response(serialize([product]))
        except:
            return send_response("Problème lors de la mise à jour.", 500)


@csrf_exempt
def in_product(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if update_stock_product(data[0], data[1], "+"):
            return send_response(True)
        else:
            return send_response("Erreur lors de la mise à jour du produit.", 500)


@csrf_exempt
def out_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if update_stock_product(data[0], data[1], "-"):
            return send_response(True)
        else:
            return send_response("Erreur lors de la mise à jour du produit.", 500)


def update_stock_product(uuid, quantity, operation):
    try:
        prod = Product.objects.get(prod_uuid=uuid)
        if operation == "+":
            prod.prod_stock = int(prod.prod_stock) + int(quantity)
        elif operation == "-":
            create_sell(prod, quantity)
            prod.prod_stock = int(prod.prod_stock) - int(quantity)

        prod.save()
        return True
    except:
        return False


def create_sell(product, quantity):
    sell = Sell()
    sell.user = User.objects.order_by("-last_login")[0]
    sell.product = product
    sell.tva = TVA.objects.get(id=product.tva_id)
    sell.price = product.prod_sellprice
    sell.qte = quantity
    sell.save()


@csrf_exempt
def in_product_store(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if update_stock_product_store(data[0], data[1], "+"):
            return send_response(True)
        else:
            return send_response("Erreur lors de la mise à jour du produit.", 500)


@csrf_exempt
def out_product_store(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if update_stock_product_store(data[0], data[1], "-"):
            return send_response(True)
        else:
            return send_response("Erreur lors de la mise à jour du produit.", 500)


def update_stock_product_store(uuid, quantity, operation):
    try:
        prod = Product.objects.get(prod_uuid=uuid)
        if operation == "+":
            prod.prod_stock_store = int(prod.prod_stock_store) + int(quantity)
        elif operation == "-":
            prod.prod_stock_store = int(prod.prod_stock_store) - int(quantity)

        prod.save()
        return True

    except:
        return False


def line_prod(request, uuid):
    prod = Product.objects.get(prod_uuid=uuid)
    linesprod = LineProduct.objects.filter(product_id=prod.id)
    lines = []

    for line in linesprod:
        lines.append(
            [line.action.action_name, line.user.username, line.date_modification.strftime("%d/%m/%Y à %H:%M:%S")])

    return send_response(lines)
