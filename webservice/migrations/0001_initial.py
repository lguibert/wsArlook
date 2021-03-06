# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_firstname', models.CharField(max_length=50)),
                ('client_lastname', models.CharField(max_length=50)),
                ('client_phone', models.CharField(max_length=20, null=True)),
                ('client_address', models.TextField(null=True)),
                ('client_town', models.CharField(max_length=40, null=True)),
                ('client_zipcode', models.CharField(max_length=10, null=True)),
                ('client_email', models.CharField(max_length=100, null=True)),
                ('client_uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='LineClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('action', models.ForeignKey(to='webservice.Action')),
                ('client', models.ForeignKey(to='webservice.Client')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LineProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('action', models.ForeignKey(to='webservice.Action')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_name', models.CharField(max_length=50)),
                ('prod_uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('prod_sellprice', models.DecimalField(max_digits=6, decimal_places=2)),
                ('prod_buyprice', models.DecimalField(max_digits=6, decimal_places=2)),
                ('prod_datebuy', models.DateField()),
                ('prod_stock', models.IntegerField()),
                ('prod_stock_store', models.IntegerField()),
                ('prod_image', models.TextField(null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('qte', models.IntegerField()),
                ('product', models.ForeignKey(to='webservice.Product')),
            ],
        ),
        migrations.CreateModel(
            name='TVA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tva_value', models.DecimalField(max_digits=4, decimal_places=2)),
                ('tva_uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visit_date', models.DateField(auto_now=True)),
                ('value', models.DecimalField(max_digits=6, decimal_places=2)),
                ('client', models.ForeignKey(to='webservice.Client')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='sell',
            name='tva',
            field=models.ForeignKey(to='webservice.TVA'),
        ),
        migrations.AddField(
            model_name='sell',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lineproduct',
            name='product',
            field=models.ForeignKey(to='webservice.Product'),
        ),
        migrations.AddField(
            model_name='lineproduct',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
