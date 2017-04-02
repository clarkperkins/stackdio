# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-02 21:22
from __future__ import unicode_literals

import stackdio.core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0004_0_8_0_migrations'),
    ]

    operations = [
        # Add the properties field first
        migrations.AddField(
            model_name='cloudaccount',
            name='global_orchestration_properties',
            field=stackdio.core.fields.JSONField(verbose_name='Global Orchestration Properties'),
        ),
    ]
