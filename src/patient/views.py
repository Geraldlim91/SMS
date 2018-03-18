import os
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.db import connection
from django.http import HttpResponse
from django.db.models import Q
from django.utils.timezone import localtime
from src.util.customfunc import isInt, get_or_none,djangoDate
from src.login.decorator import login_active_required
from models import Patient, Patient_Record
from forms import AddPatientForm
from datetime import date, time

# @login_active_required(login_url=reverse_lazy('src.login'))
def patientView(request, msgNote=""):
    otherVars = {}
    displayMsg = None
    if msgNote:
        displayMsg = msgNote
    elif 'msgNote' in request.session:
        displayMsg = request.session['msgNote']


    numOfRecords = Patient.objects.count()
    patientObject = Patient.objects.all().order_by('nric')[:10]
    patientList = []
    for patientObj in patientObject:
        patientList.append([
            patientObj.nric,
            patientObj.full_name,
            patientObj.gender,
            str(patientObj.age),
            str(patientObj.visit_time),
        ])
    tableInfo = {'patientList': json.dumps(patientList), 'numOfRecords': numOfRecords}

    if len(patientList) > 0:
        tableInfo['recordStart'] = 1
        tableInfo['recordEnd'] = len(patientList)
    if numOfRecords > 10:
        tableInfo['nextEnabled'] = 'Y'


    # Message to display when delete is pressed (<title>,<body>)
    delMsg = ('Delete user(s)?', 'user(s) will be permanently deleted and cannot be recovered. \
              You can consider inactivating the accounts instead. Are you sure you want to proceed to delete the users?')

    # Message to display when table has no records
    tabEmptyMsg = 'No user accounts available for viewing'
    return render(request, 'main/patientview.html', {'otherVars': otherVars, 'tableInfo': tableInfo, 'delMsg': delMsg, 'tabEmptyMsg': tabEmptyMsg})


# @login_active_required(login_url=reverse_lazy('login'))
def patientViewUpdate(request):
    if request.method == 'POST':
        sortingNames = ['nric', 'full_name', 'gender', 'age', 'visit_time',]
        sortOrder = []
        for val in json.loads(request.POST['sortingType']):
            sortOrder.append(('-' if val['order'] == 1 else '') + sortingNames[val['value']])

        query = Q()
        if 'searchText' in request.POST:
            searchText = json.loads(request.POST['searchText'])
            tSearchArr = []
            fInputArr = []
            for sItem in searchText:
                if sItem['searchType'] == 'sText':
                    tSearchArr = [('nric__icontains', sItem['searchTerm']),
                                  ('full_name__icontains', sItem['searchTerm']),
                                  ('gender__icontains', sItem['searchTerm']),
                                  ('age__icontains', sItem['searchTerm']),
                                  ('visit_time__icontains', sItem['searchTerm'])]

                    if isInt(sItem['searchTerm']):
                        tSearchArr.append(('nric', int(sItem['searchTerm'])))
            for item in [Q(x) for x in tSearchArr]:
                query |= item
            for item in [Q(x) for x in fInputArr]:
                query &= item

        if query:
            numOfRecords = Patient.objects.filter(query).count()
        else:
            numOfRecords = Patient.objects.count()

        recordStart = int(request.POST['recordStart'])
        recordEnd = int(request.POST['recordEnd'])
        pageLength = int(request.POST['pageLength'])

        if 'paginate' in request.POST:
            paginate = request.POST['paginate']
            if paginate == 'next':
                recordStart = recordEnd + 1
            elif paginate == 'prev':
                recordStart -= pageLength
            elif paginate == 'first':
                recordStart = 1
            elif paginate == 'last':
                recordStart = numOfRecords - pageLength + 1
        if recordStart > numOfRecords:
            recordStart = numOfRecords
        if recordStart < 1 or 'firstSearch' in request.POST:
            recordStart = 1
        if query:
            # profileObjects = User_Profile.objects.filter(query).order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]
            patientObjects = Patient.objects.filter(query).order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]
        else:
            # profileObjects = User_Profile.objects.all().order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]
            patientObjects = Patient.objects.all().order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]

        listLength = len(patientObjects)
        userList = []
        for patientObj in patientObjects:
            userList.append([
                patientObj.nric,
                patientObj.full_name,
                patientObj.gender,
                str(patientObj.age),
                str(patientObj.visit_time),
            ])

        tableInfo = {'valueList': userList, 'numOfRecords': numOfRecords}
        if listLength > 0:
            recordEnd = recordStart + listLength - 1
            if recordStart > 1:
                tableInfo['prevEnabled'] = 'Y'
            if recordEnd < numOfRecords:
                tableInfo['nextEnabled'] = 'Y'
        else:
            recordStart = 0
            recordEnd = 0
        tableInfo['recordStart'] = recordStart
        tableInfo['recordEnd'] = recordEnd
        return HttpResponse(json.dumps(tableInfo))
    else:
        return HttpResponseRedirect(reverse('patientView'))


# @login_active_required(login_url=reverse_lazy('login'))
def patientAdd(request):
    otherVars = {'pageType':'addPatient'}
    print request.method

    # if request method is post
    if request.method == 'POST':
        addPatientForm = AddPatientForm(request.POST)

        # input validation for add user and user profile form
        if addPatientForm.is_valid():
        # save the user and user profile object into database
            patientIns = Patient()
            patientIns.nric = request.POST['nric']
            patientIns.full_name = request.POST['full_name']
            patientIns.contact_num = request.POST['contact_num']
            patientIns.gender = request.POST['gender']
            patientIns.dob = request.POST['dob']
            patientIns.address = request.POST['address']
            patientIns.postalcode = request.POST['postalcode']
            patientIns.nok = request.POST['nok']
            patientIns.age =  date.today().year - int(str(patientIns.dob).split('-')[0])
            patientIns.email = request.POST['email']
            patientIns.allergy = request.POST['allergy']
            patientIns.visit_time = time()
            patientIns.save()
            return HttpResponseRedirect(reverse('patientView'))
    else:
        addPatientForm = AddPatientForm()

    # Define header groups
    hgrps = ({'name':'Patient Information','lblwidth':'160'}, {'name':'Next-of-Kin Information','lblwidth':'160'},)
    # For first header group
    addPatientForm.fields["nric"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["nric"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["full_name"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["full_name"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["contact_num"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["contact_num"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["gender"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["gender"].widget.attrs['wsize'] = '300'

    # # For first header group
    addPatientForm.fields["dob"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["dob"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["address"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["address"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["postalcode"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["postalcode"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["email"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["email"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["allergy"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["allergy"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["nok"].widget.attrs['hgrp'] = '1'
    addPatientForm.fields["nok"].widget.attrs['wsize'] = '300'


    return render(request, 'main/patientchng.html', {'otherVars':otherVars,'addPatientForm':addPatientForm,'hgrps':hgrps})

def patientEdit(request, nricvalue=None):
    patientObj = get_or_none(Patient, nric=nricvalue)
    # Define header groups
    otherVars = {'edit': 'Y'}

    # if request method is post\

    if request.method == 'POST':
        addPatientForm = AddPatientForm(request.POST)

        # input validation for add user and user profile form


            # update user information
        if addPatientForm.is_valid():
            patientObj.nric = request.POST['nric']
            patientObj.full_name = request.POST['full_name']
            patientObj.contact_num = request.POST['contact_num']
            patientObj.gender = request.POST['gender']
            patientObj.dob = request.POST['dob']
            patientObj.address = request.POST['address']
            patientObj.postalcode = request.POST['postalcode']
            patientObj.nok = request.POST['nok']
            patientObj.age = date.today().year - int(str(patientObj.dob).split('-')[0])
            patientObj.email = request.POST['email']
            patientObj.allergy = request.POST['allergy']
            patientObj.save()
            return HttpResponseRedirect(reverse('patientView'))
    else:
        addPatientForm = AddPatientForm(initial={
            'nric': patientObj.nric,
            'full_name': patientObj.full_name,
            'contact_num': patientObj.contact_num,
            'gender': patientObj.gender,
            'dob': patientObj.dob,
            'address': patientObj.address,
            'postalcode': patientObj.postalcode,
            'nok': patientObj.nok,
            'email': patientObj.email,
            'allergy': patientObj.allergy,
        })
        # For first header group
    addPatientForm.fields["nric"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["nric"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["full_name"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["full_name"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["contact_num"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["contact_num"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["gender"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["gender"].widget.attrs['wsize'] = '300'

    # For first header group
    addPatientForm.fields["dob"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["dob"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["address"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["address"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["postalcode"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["postalcode"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["email"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["email"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["allergy"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["allergy"].widget.attrs['wsize'] = '300'

    addPatientForm.fields["nok"].widget.attrs['hgrp'] = '1'
    addPatientForm.fields["nok"].widget.attrs['wsize'] = '300'

    hgrps = ({'name': 'Patient Information', 'lblwidth': '160'}, {'name': 'Next-of-Kin Information', 'lblwidth': '160'},)

    numOfRecords = Patient_Record.objects.filter(nric=nricvalue).count()
    caseObject = Patient_Record.objects.filter(nric=nricvalue).order_by('-record_create_datetime')[:10]
    caseList = []
    for caseObj in caseObject:
        caseList.append([
            caseObj.id,
            caseObj.symptoms,
            caseObj.diagnosis,
            str(caseObj.record_create_datetime),
        ])
    tableInfo = {'caseList': json.dumps(caseList), 'numOfRecords': numOfRecords}

    if len(caseList) > 0:
        tableInfo['recordStart'] = 1
        tableInfo['recordEnd'] = len(caseList)
    if numOfRecords > 10:
        tableInfo['nextEnabled'] = 'Y'
    # Message to display when table has no records
    tabEmptyMsg = 'Patient has no previous medical case to show'
    return render(request, 'main/patientchng.html', {'otherVars': otherVars, 'hgrps': hgrps, 'addPatientForm': addPatientForm,'tableInfo': tableInfo,'tabEmptyMsg': tabEmptyMsg,})


