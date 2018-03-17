# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-17 17:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('nric', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=200)),
                ('postalcode', models.CharField(max_length=10)),
                ('nok', models.CharField(max_length=100)),
                ('allergy', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='Patient_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_description', models.TextField()),
                ('medical_history', models.TimeField()),
                ('nric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.Patient')),
            ],
            options={
                'db_table': 'patient_record',
            },
        ),
    ]
