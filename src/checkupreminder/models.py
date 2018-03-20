# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class NotificationCriteria(models.Model):
    id = models.AutoField(primary_key=True)
    screeningName = models.CharField(max_length=100)
    gender = models.CharField(max_length=8,null=True)
    agegrp = models.CharField(max_length=10)
    description = models.TextField(null=False)
    message = models.TextField(null=False)

    class Meta:
        db_table = 'notificationcriteria'