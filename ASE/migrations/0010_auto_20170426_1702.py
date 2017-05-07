# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASE', '0009_courserequest_facultyrequest_projectrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Visible'),
        ),
        migrations.AddField(
            model_name='project',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Visible'),
        ),
    ]
