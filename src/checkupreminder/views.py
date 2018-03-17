# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse,reverse_lazy
from forms import reminderForm
from django.shortcuts import render


# Create your views here.
def reminder(request):
    otherVars = {'pageType' : 'checkup'}

    if request.method == 'POST':
        remForm = reminderForm(request.POST)
        screenings = request.POST.getlist('screening')
        for s in screenings:
            print s

        if remForm.is_valid():
            screenings = remForm.cleaned_data.get('screenings')



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