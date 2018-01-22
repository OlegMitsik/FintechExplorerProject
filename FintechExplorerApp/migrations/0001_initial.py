# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Taxonomy_Node',
            fields=[
                ('Identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('Parent', models.IntegerField()),
                ('Name', models.CharField(max_length=127)),
                ('IsCategory', models.BooleanField(default=False)),
                ('Description', models.CharField(max_length=255)),
            ],
        ),
    ]