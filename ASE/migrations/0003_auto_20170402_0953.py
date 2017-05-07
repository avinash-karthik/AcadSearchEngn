# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-02 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASE', '0002_auto_20170401_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='student',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='Website'),
        ),
    ]
