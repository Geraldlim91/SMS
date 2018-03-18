# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import simplejson as json

from django.shortcuts import render


# Create your views here.
with open('../util/json/symptoms.json') as json_data:
    data = json.load(json_data)
    st = "Anxiety"
    d = data[1][st]
    print d

