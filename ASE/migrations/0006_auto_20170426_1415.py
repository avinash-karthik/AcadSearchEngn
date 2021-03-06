# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 14:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ASE', '0005_auto_20170425_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], max_length=10, verbose_name='Status')),
                ('feedback', models.CharField(blank=True, max_length=200, verbose_name='Feedback')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='request',
            name='user',
        ),
        migrations.AddField(
            model_name='faculty',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Visible'),
        ),
        migrations.AddField(
            model_name='student',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Visible'),
        ),
        migrations.DeleteModel(
            name='Request',
        ),
        migrations.AddField(
            model_name='studentrequest',
            name='data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ASE.Student', verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='studentrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
