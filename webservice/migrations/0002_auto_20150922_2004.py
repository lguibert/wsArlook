# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_lastmodification',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_buyprice',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_lastmodification',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_sellprice',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2),
        ),
    ]
