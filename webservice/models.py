from django.db import models
from django.contrib.auth.models import User
from uuidfield import UUIDField
from django.db.models.signals import post_save, pre_save


class TVA(models.Model):
    tva_value = models.DecimalField(max_digits=4, decimal_places=2)
    tva_uuid = UUIDField(auto=True)

    def __unicode__(self):
        return self.tva_value


class Product(models.Model):
    prod_name = models.CharField(max_length=50)
    prod_uuid = UUIDField(auto=True)
    prod_sellprice = models.DecimalField(max_digits=6, decimal_places=2)
    prod_buyprice = models.DecimalField(max_digits=6, decimal_places=2)
    prod_datebuy = models.DateField()
    prod_stock = models.IntegerField()
    prod_stock_store = models.IntegerField()
    prod_image = models.TextField(null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.prod_name


class Action(models.Model):
    action_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.action_name


class Client(models.Model):
    client_firstname = models.CharField(max_length=50)
    client_lastname = models.CharField(max_length=50)
    client_phone = models.CharField(max_length=20, null=True)
    client_address = models.TextField(null=True)
    client_town = models.CharField(max_length=40, null=True)
    client_zipcode = models.CharField(max_length=10, null=True)
    client_email = models.CharField(max_length=100, null=True)
    client_uuid = UUIDField(auto=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.client_firstname + " " + self.client_lastname


class TypePay(models.Model):
    name = models.CharField(max_length=50)


class Visit(models.Model):
    visit_date = models.DateField(auto_now=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)

    typepay = models.ForeignKey(TypePay)


class LineProduct(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    action = models.ForeignKey(Action)
    date_modification = models.DateTimeField(auto_now=True)


class LineClient(models.Model):
    user = models.ForeignKey(User)
    client = models.ForeignKey(Client)
    action = models.ForeignKey(Action)
    date_modification = models.DateTimeField(auto_now=True)


def create_line_product(sender, instance, created, **kwargs):
    lp = LineProduct()
    lp.user = User.objects.order_by("-last_login")[0]
    lp.product = instance

    if created:
        lp.action = Action.objects.get(id=2)
    else:
        lp.action = Action.objects.get(id=1)

    lp.save()


def create_line_client(sender, instance, created, **kwargs):
    lc = LineClient()
    lc.user = User.objects.order_by("-last_login")[0]
    lc.client = instance

    if created:
        lc.action = Action.objects.get(id=2)
    else:
        lc.action = Action.objects.get(id=1)

    lc.save()


# ------------------------ BILAN ZONE ------------------------
class Sell(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    tva = models.ForeignKey(TVA)
    date = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    qte = models.IntegerField()

    typepay = models.ForeignKey(TypePay)


post_save.connect(create_line_product, sender=Product)
post_save.connect(create_line_client, sender=Client)
