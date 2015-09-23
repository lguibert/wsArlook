# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0002_auto_20150922_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prod_uuid',
            field=uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_buyprice',
            field=models.DecimalField(max_digits=6, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_sellprice',
            field=models.DecimalField(max_digits=6, decimal_places=2),
        ),
    ]
