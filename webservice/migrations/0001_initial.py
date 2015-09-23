# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_firstname', models.CharField(max_length=50)),
                ('client_lastname', models.CharField(max_length=50)),
                ('client_phone', models.CharField(max_length=20)),
                ('client_address', models.TextField()),
                ('client_town', models.CharField(max_length=40)),
                ('client_zipcode', models.CharField(max_length=10)),
                ('client_email', models.CharField(max_length=100)),
                ('client_lastmodification', models.DateTimeField()),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_name', models.CharField(max_length=50)),
                ('prod_description', models.TextField()),
                ('prod_sellprice', models.DecimalField(max_digits=6, decimal_places=2)),
                ('prod_buyprice', models.DecimalField(max_digits=6, decimal_places=2)),
                ('prod_datebuy', models.DateField()),
                ('prod_stock', models.IntegerField()),
                ('prod_lastmodification', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TVA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tva_value', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tva',
            field=models.ForeignKey(to='webservice.TVA'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
