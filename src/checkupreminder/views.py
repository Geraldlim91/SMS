# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse,reverse_lazy
from forms import reminderForm
from django.shortcuts import render
from models import NotificationCriteria
from src.util.mail import SendMail
from ..patient.models import Patient

# Create your views here.
def reminder(request):
    otherVars = {'pageType' : 'checkup'}

    if request.method == 'POST':
        remForm = reminderForm(request.POST)
        screenings = request.POST.getlist('screening')
        for s in screenings:
            receipentGrp = NotificationCriteria.objects.get(screeningName=s)
            agegroup = receipentGrp.agegrp
            gender = receipentGrp.gender
            message = receipentGrp.message
            l_age,u_age = agegroup.split("-")
            l_age = int(l_age)
            u_age = int(u_age)
            patientObject = Patient.objects.all().order_by('nric')
            for p in patientObject:
                p_gender = p.gender
                p_age = int(p.age)
                p_email = p.email
                if gender is None:
                    if p_age >= l_age and p_age <= u_age:
                        SendMail(p_email,"Screening Reminder",message)

                else:
                    if p_age >= l_age and p_age <= u_age and p_gender == gender:
                        SendMail(p_email,"Screening Reminder",message)





    else:
        remForm = reminderForm()


        # input validation for add user and user profile form
        #if remForm.is_valid():
            # userIns = User_Profile()
            # userIns.email = request.POST['email']
            # userIns.username = userIns.email
            # userIns.set_password(request.POST['password'])
            # userIns.first_name = request.POST['first_name']
            # userIns.last_name = request.POST['last_name']
            # if userIns.contact_num == None:
            #    userIns.contact_num = 'N.A'
            # else:
            #     userIns.contact_num = request.POST['contact_num']
            # if userIns.company == None:
            #     userIns.company = 'N.A'
            # else:
            #     userIns.company = request.POST['company']
            #
            # userIns.save()
            # return HttpResponseRedirect(reverse('login'))
        #else:
           # pass

    #else:
        #remForm = reminderForm()

# Define header groups
    hgrps = ({'name':'Type of check up','lblwidth':'160'},)
   # remForm.fields["checkup1"].widget.attrs['hgrp'] = '0'
   # remForm.fields["checkup1"].widget.attrs['wsize'] = '100'

    return render(request, 'main/checkupreminder.html', {'otherVars': otherVars, 'hgrps': hgrps})