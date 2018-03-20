# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from forms import addScreeningForm
from django.shortcuts import render
from models import NotificationCriteria
from src.util.mail import SendMail
from ..patient.models import Patient
from src.login.decorator import login_active_required


@login_active_required(login_url=reverse_lazy('login'))
def reminder(request):
    otherVars = {'pageType': 'logon', 'UserInfo': request.user.first_name}

    if request.method == 'POST':
        # remForm = reminderForm(request.POST)
        screenings = request.POST.getlist('screening')
        if not request.POST.getlist('screening') :
            otherVars.update({'msgNote':'Please select a input'})

        for s in screenings:
            receipentGrp = NotificationCriteria.objects.get(id=int(s))
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
                if p.gender == None:
                    if p_age >= l_age and p_age <= u_age:
                        SendMail(pArray,"Screening Reminder",message)
                else:
                    if p_age >= l_age and p_age <= u_age and p_gender == gender:
                        SendMail(pArray,"Screening Reminder",message)
            otherVars.update({'msgNote': 'Send Complete'})
    else:
        pass

# Define header groups
    screentable = []
    screen = NotificationCriteria.objects.all().order_by('id')
    for i in screen:
        screentable.append({'screening_name':i.screeningName, 'value':i.id, 'description': i.description})
    hgrps = ({'name':'Type of check up','lblwidth':'400'},)

    return render(request, 'main/checkupreminder.html', {'otherVars': otherVars, 'hgrps': hgrps, 'screenTable':screentable})

@login_active_required(login_url=reverse_lazy('login'))
def addScreening(request):
    otherVars = {'pageType': 'logon', 'UserInfo': request.user.first_name}
    # if request method is post
    if request.method == 'POST':
        addnewscreening = addScreeningForm(request.POST)
        # input validation for add user and user profile form
        if addnewscreening.is_valid():
            # save the newscreening object into database
            newrecord = NotificationCriteria()
            newrecord.screeningName = request.POST['screening_name']
            newrecord.agegrp = request.POST['age_grp']
            if request.POST['gender'] == "Both":
                newrecord.gender = None
            else:
                newrecord.gender = request.POST['gender']
            newrecord.description = request.POST['description']
            newrecord.message = request.POST['message']
            newrecord.save()
            return HttpResponseRedirect(reverse('screenReminder'))
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
    addnewscreening.fields["gender"].widget.attrs['wsize'] = '120'

    addnewscreening.fields["description"].widget.attrs['hgrp'] = '0'
    addnewscreening.fields["description"].widget.attrs['wsize'] = '300'

    addnewscreening.fields["message"].widget.attrs['hgrp'] = '0'
    addnewscreening.fields["message"].widget.attrs['wsize'] = '300'

    return render(request, 'main/addscreeningform.html', {'otherVars':otherVars,'addscreeningform':addnewscreening,'hgrps':hgrps})
