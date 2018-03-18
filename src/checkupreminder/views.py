# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse,reverse_lazy
from forms import reminderForm,addScreeningForm
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
            print str(s)
            receipentGrp = NotificationCriteria.objects.get(screeningName=s)
            agegroup = receipentGrp.agegrp
            gender = receipentGrp.gender
            message = receipentGrp.message
            l_age,u_age = agegroup.split("-")
            l_age = int(l_age)
            u_age = int(u_age)
            pArray = []
            patientObject = Patient.objects.all().order_by('nric')
            for p in patientObject:
                p_gender = p.gender
                p_age = int(p.age)
                pArray.append(p.email)
                if gender is None:
                    if p_age >= l_age and p_age <= u_age:
                        SendMail(pArray,"Screening Reminder",message)
                else:
                    if p_age >= l_age and p_age <= u_age and p_gender == gender:
                        SendMail(pArray,"Screening Reminder",message)





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
    screentable = []
    screen = NotificationCriteria.objects.all()
    for i in screen:
        screentable.append({'description':i.description, 'value':i.screeningName})
    hgrps = ({'name':'Type of check up','lblwidth':'160'},)
   # remForm.fields["checkup1"].widget.attrs['hgrp'] = '0'
   # remForm.fields["checkup1"].widget.attrs['wsize'] = '100'

    return render(request, 'main/checkupreminder.html', {'otherVars': otherVars, 'hgrps': hgrps, 'screenTable':screentable})

def addScreening(request):
    otherVars = {'pageType':'addscreeningforreminder'}
    # if request method is post
    if request.method == 'POST':
        addnewscreening = addScreeningForm(request.POST)

        # input validation for add user and user profile form
        if addnewscreening.is_valid():
            # save the user and user profile object into database
            newrecord = NotificationCriteria()
            newrecord.screeningName = request.POST['screening_name']
            newrecord.agegrp = request.POST['age_grp']
            newrecord.gender = request.POST['gender']
            newrecord.description = request.POST['description']
            newrecord.message = request.POST['message']
            newrecord.save()
        else:
            pass
    else:
        addnewscreening = addScreeningForm()

    # Define header groups
    hgrps = ({'name':'Screening Notification Criteria','lblwidth':'160'},)
    # For first header group
    addnewscreening.fields["screening_name"].widget.attrs['hgrp'] = '0'
    addnewscreening.fields["screening_name"].widget.attrs['wsize'] = '300'

    addnewscreening.fields["age_grp"].widget.attrs['hgrp'] = '0'
    addnewscreening.fields["age_grp"].widget.attrs['wsize'] = '300'

    addnewscreening.fields["gender"].widget.attrs['hgrp'] = '0'
    addnewscreening.fields["gender"].widget.attrs['wsize'] = '300'

    addnewscreening.fields["description"].widget.attrs['hgrp'] = '0'
    addnewscreening.fields["description"].widget.attrs['wsize'] = '300'

    addnewscreening.fields["message"].widget.attrs['hgrp'] = '0'
    addnewscreening.fields["message"].widget.attrs['wsize'] = '300'

    # For first header group
    # addnewscreening.fields["dob"].widget.attrs['hgrp'] = '0'
    # addnewscreening.fields["dob"].widget.attrs['wsize'] = '300'
    #
    # addnewscreening.fields["address"].widget.attrs['hgrp'] = '0'
    # addnewscreening.fields["address"].widget.attrs['wsize'] = '300'
    #
    # addnewscreening.fields["postalcode"].widget.attrs['hgrp'] = '0'
    # addnewscreening.fields["postalcode"].widget.attrs['wsize'] = '300'
    #
    # addnewscreening.fields["email"].widget.attrs['hgrp'] = '0'
    # addnewscreening.fields["email"].widget.attrs['wsize'] = '300'
    #
    # addnewscreening.fields["allergy"].widget.attrs['hgrp'] = '0'
    # addnewscreening.fields["allergy"].widget.attrs['wsize'] = '300'
    #
    # addnewscreening.fields["nok"].widget.attrs['hgrp'] = '1'
    # addnewscreening.fields["nok"].widget.attrs['wsize'] = '300'

    return render(request, 'main/addscreeningform.html', {'otherVars':otherVars,'addscreeningform':addnewscreening,'hgrps':hgrps})
