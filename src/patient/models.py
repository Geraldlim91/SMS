from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import django
import datetime


class Patient(models.Model):
    nric = models.CharField(primary_key=True, unique=True, max_length=9)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=200)
    postalcode = models.CharField(max_length=10)
    nok = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    allergy = models.CharField(max_length=100)
    contact_num = models.CharField(max_length=20)
    visit_time = models.TimeField(default=django.utils.timezone.now)

    class Meta:
        db_table = 'patient'


class Patient_Record(models.Model):
    id = models.AutoField(primary_key=True)
    nric = models.ForeignKey(Patient)
    medical_description = models.TextField()
    medical_history = models.TextField()
    symptoms = models.TextField()
    diagnosis = models.TextField()
    record_create_datetime = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        db_table = 'patient_record'
