# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-14 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stacks', '0008_0_8_0_migrations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='instance_id',
            field=models.CharField(blank=True, max_length=64, verbose_name='Instance ID'),
        ),
        migrations.AlterField(
            model_name='host',
            name='sir_id',
            field=models.CharField(default='unknown', max_length=64, verbose_name='SIR ID'),
        ),
    ]
