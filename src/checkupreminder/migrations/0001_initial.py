# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-19 04:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationCriteria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('screeningName', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=12, null=True)),
                ('agegrp', models.CharField(max_length=10)),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'notificationcriteria',
            },
        ),
    ]
