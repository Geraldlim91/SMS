# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-18 20:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, unique=True)),
                ('contact_num', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
