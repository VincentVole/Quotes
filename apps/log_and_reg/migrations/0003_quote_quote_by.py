# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_and_reg', '0002_auto_20170721_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='quote_by',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
