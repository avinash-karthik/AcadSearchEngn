# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASE', '0012_auto_20170426_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='feedback',
            field=models.TextField(blank=True, max_length=200, verbose_name='Feedback'),
        ),
    ]
