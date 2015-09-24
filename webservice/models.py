from django.db import models
from django.contrib.auth.models import User
from uuidfield import UUIDField


class TVA(models.Model):
    tva_value = models.DecimalField(max_digits=4, decimal_places=2)
    tva_uuid = UUIDField(auto=True)

    def __unicode__(self):
        return self.tva_value


class Product(models.Model):
    prod_name = models.CharField(max_length=50)
    prod_uuid = UUIDField(auto=True)
    prod_description = models.TextField()
    prod_sellprice = models.DecimalField(max_digits=6, decimal_places=2)
    prod_buyprice = models.DecimalField(max_digits=6, decimal_places=2)
    prod_datebuy = models.DateField()
    prod_stock = models.IntegerField()
    prod_lastmodification = models.DateTimeField(auto_now=True)
    prod_image = models.TextField()

    user = models.ManyToManyField(User)
    tva = models.ForeignKey(TVA)

    def __unicode__(self):
        return self.prod_name


class Client(models.Model):
    client_firstname = models.CharField(max_length=50)
    client_lastname = models.CharField(max_length=50)
    client_phone = models.CharField(max_length=20, null=True)
    client_address = models.TextField(null=True)
    client_town = models.CharField(max_length=40, null=True)
    client_zipcode = models.CharField(max_length=10, null=True)
    client_email = models.CharField(max_length=100, null=True)
    client_lastmodification = models.DateTimeField(auto_now=True)
    client_uuid = UUIDField(auto=True)

    user = models.ManyToManyField(User)

    def __unicode__(self):
        return self.client_firstname + " " + self.client_lastname

