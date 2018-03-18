# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import simplejson as json

from django.shortcuts import render


# Create your views here.
def symptomcheck(symptoms):
    diagnoses = []
    with open('../util/json/symptoms.json') as json_data:
        data = json.load(json_data)
        for d in data:
            for s in symptoms:
                if (d.has_key(s)):
                    diagnoses.append(d)

    json_data.close()
    return diagnoses
                    # for i in d[s]:
                    #     diagnoses.append(i)





        #for d in data:
            #for s symptoms:


        #for key,value in data.items():
            #print key
            # for s in symptoms:
            #     if s == value[s]:
            #         diagnoses = value[s]
            #         print diagnoses

        #return diagnoses

