# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-26 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_resettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('Input', 'Input'), ('Accepted', 'Accepted')], default='Input', max_length=255),
        ),
    ]
