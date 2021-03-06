import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from src.util.customfunc import isInt, get_or_none
from src.login.decorator import login_active_required
from models import Patient, Patient_Record
from forms import AddPatientForm,AddPatientCaseForm, IssueDictonaryForm
from datetime import date, time
from src.util.customfunc import symptomcheck,issueinformation

@login_active_required(login_url=reverse_lazy('login'))
def patientView(request, msgNote=""):
    otherVars = {'pageType': 'logon', 'UserInfo': request.user.first_name}

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
            '<span class=\'btn btn-info\' style="cursor:pointer;" onclick=\"javascript:window.location.href=\'/main/patient/case/add/%s\'\"><b>&nbsp;+ Case</b></span>' % patientObj.nric
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


@login_active_required(login_url=reverse_lazy('login'))
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
                '<span class=\'btn btn-info\' style="cursor:pointer;" onclick=\"javascript:window.location.href=\'/main/patient/case/add/%s\'\"><b>&nbsp;+ Case</b></span>' % patientObj.nric
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


@login_active_required(login_url=reverse_lazy('login'))
def patientAdd(request):
    otherVars = {'pageType': 'logon', 'UserInfo': request.user.first_name}

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
    addPatientForm.fields["gender"].widget.attrs['wsize'] = '120'

    # # For first header group
    addPatientForm.fields["dob"].widget.attrs['hgrp'] = '0'
    addPatientForm.fields["dob"].widget.attrs['wsize'] = '150'

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

@login_active_required(login_url=reverse_lazy('login'))
def patientEdit(request, nricvalue=None):
    otherVars = {'pageType': 'logon', 'UserInfo': request.user.first_name,'edit': 'Y', 'nric':nricvalue}
    patientObj = get_or_none(Patient, nric=nricvalue)
    if request.method == 'POST':
        addPatientForm = AddPatientForm(request.POST)
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

@login_active_required(login_url=reverse_lazy('login'))
def caseViewUpdate(request, nricvalue=None):

    if request.method == 'POST':
        sortingNames = ['id', 'symptoms', 'diagnosis', 'record_create_datetime',]
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
                    tSearchArr = [('id__icontains', sItem['searchTerm']),
                                  ('symptoms__icontains', sItem['searchTerm']),
                                  ('diagnosis__icontains', sItem['searchTerm']),
                                  ('record_create_datetime__icontains', sItem['searchTerm'])]

                    if isInt(sItem['searchTerm']):
                        tSearchArr.append(('id', int(sItem['searchTerm'])))
            for item in [Q(x) for x in tSearchArr]:
                query |= item
            for item in [Q(x) for x in fInputArr]:
                query &= item

        if query:
            numOfRecords = Patient_Record.objects.filter(nric=nricvalue).filter(query).count()
        else:
            numOfRecords = Patient_Record.objects.filter(nric=nricvalue).count()

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
            caseObjects = Patient_Record.objects.filter(nric=nricvalue).filter(query).order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]
        else:
            caseObjects = Patient_Record.objects.filter(nric=nricvalue).order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]

        listLength = len(caseObjects)
        caseList = []
        for caseObj in caseObjects:
            caseList.append([
                caseObj.id,
                caseObj.symptoms,
                caseObj.diagnosis,
                str(caseObj.record_create_datetime),
            ])

        tableInfo = {'valueList': caseList, 'numOfRecords': numOfRecords}
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
        return HttpResponseRedirect(reverse('patientEdit', kwargs={'nricvalue': nricvalue}))

@login_active_required(login_url=reverse_lazy('login'))
def patientCaseAdd(request, nricvalue=None ):
    otherVars = {'pageType': 'logon', 'UserInfo': request.user.first_name}
    # if request method is post
    hgrps = ({'name':'Symptoms Checker','lblwidth':'160', 'value':'1'},{'name':'Case Information','lblwidth':'160'},)
    if request.method == 'POST':
        addPatientCaseForm = AddPatientCaseForm(request.POST)
        # input validation for add user and user profile form
        if str(request.POST).__contains__("Generate"):
            recordIns = Patient_Record()
            recordIns.symptoms = str(request.POST['symptoms']).lower()
            symptoms = str(request.POST['symptoms']).split(',')
            list_dict = symptomcheck(symptoms)
            if list_dict == []:
                d = 'Cannot find Symptoms'
            else:
                d = ''
                for dig in list_dict:
                    d += dig + '\n'

            addPatientCaseForm = AddPatientCaseForm(initial={
                'nric': nricvalue,
                'symptoms':recordIns.symptoms,
                'diagnosis':'List of Possible Diagnosis: ' + '\n' + '\n' + d})


        elif addPatientCaseForm.is_valid() and not str(request.POST).__contains__('Generate'):
        # save the user and user profile object into database
            recordIns = Patient_Record()
            recordIns.nric_id = nricvalue
            recordIns.medical_description = request.POST['medical_description']
            recordIns.medical_history = request.POST['medical_history']
            recordIns.symptoms = request.POST['symptoms']
            recordIns.diagnosis = request.POST['diagnosis']
            recordIns.visit_time = time()
            recordIns.save()

            return HttpResponseRedirect(reverse('patientEdit', kwargs={'nricvalue': nricvalue}))
    else:
        addPatientCaseForm = AddPatientCaseForm(initial={
            'nric': nricvalue,
            })

    # Define header groups
    # For first header group

    addPatientCaseForm.fields["symptoms"].widget.attrs['hgrp'] = '0'
    addPatientCaseForm.fields["symptoms"].widget.attrs['wsize'] = '300'

    addPatientCaseForm.fields["diagnosis"].widget.attrs['hgrp'] = '0'
    addPatientCaseForm.fields["diagnosis"].widget.attrs['wsize'] = '600'

    addPatientCaseForm.fields["nric"].widget.attrs['hgrp'] = '1'
    addPatientCaseForm.fields["nric"].widget.attrs['wsize'] = '300'

    addPatientCaseForm.fields["medical_description"].widget.attrs['hgrp'] = '1'
    addPatientCaseForm.fields["medical_description"].widget.attrs['wsize'] = '600'

    addPatientCaseForm.fields["medical_history"].widget.attrs['hgrp'] = '1'
    addPatientCaseForm.fields["medical_history"].widget.attrs['wsize'] = '600'


    return render(request, 'main/patientcaseform.html', {'otherVars':otherVars,'addPatientCaseForm':addPatientCaseForm,'hgrps':hgrps})

@login_active_required(login_url=reverse_lazy('login'))
def patientCaseView(request, idvalue=None):
    otherVars = {'pageType': 'logon', 'UserInfo': request.user.first_name,'edit': 'Y'}
    # if request method is post
    caseObj = get_or_none(Patient_Record, id=idvalue)
    hgrps = ({'name':'Symptoms Checker','lblwidth':'160', 'value':'1'},{'name':'Case Information','lblwidth':'160'},)
    if request.method == 'POST':
        addPatientCaseForm = AddPatientCaseForm(request.POST)
        # input validation for add user and user profile form
        if str(request.POST).__contains__("Generate"):
            caseIns = Patient_Record()
            caseIns.symptoms = str(request.POST['symptoms']).lower()
            symptoms = str(request.POST['symptoms']).split(',')
            list_dict = symptomcheck(symptoms)
            if list_dict == []:
                d = 'Cannot find Symptoms'
            else:
                d = ''
                for dig in list_dict:
                    d += dig + '\n'

            addPatientCaseForm = AddPatientCaseForm(initial={
                'nric': caseObj.nric_id,
                'symptoms':caseIns.symptoms,
                'diagnosis':'List of Possible Diagnosis: ' + '\n' + '\n' + d,
                'medical_description': caseObj.medical_description,
                'medical_history':caseObj.medical_history,
            })


        elif addPatientCaseForm.is_valid() and not str(request.POST).__contains__('Generate'):
        # save the user and user profile object into database
            caseIns = Patient_Record()
            caseIns.id = idvalue
            caseIns.nric_id = caseObj.nric_id
            caseIns.medical_description = request.POST['medical_description']
            caseIns.medical_history = request.POST['medical_history']
            caseIns.symptoms = request.POST['symptoms']
            caseIns.diagnosis = request.POST['diagnosis']
            caseIns.visit_time = time()
            caseIns.save()


            return HttpResponseRedirect(reverse('patientEdit', kwargs={'nricvalue':caseObj.nric_id}))
    else:
        addPatientCaseForm = AddPatientCaseForm(initial={
            'nric': caseObj.nric_id,
            'symptoms': caseObj.symptoms,
            'diagnosis': caseObj.diagnosis,
            'medical_history': caseObj.medical_history,
            'medical_description': caseObj.medical_description,
            })

    # Define header groups
    # For first header group

    addPatientCaseForm.fields["symptoms"].widget.attrs['hgrp'] = '0'
    addPatientCaseForm.fields["symptoms"].widget.attrs['wsize'] = '300'

    addPatientCaseForm.fields["diagnosis"].widget.attrs['hgrp'] = '0'
    addPatientCaseForm.fields["diagnosis"].widget.attrs['wsize'] = '600'

    addPatientCaseForm.fields["nric"].widget.attrs['hgrp'] = '1'
    addPatientCaseForm.fields["nric"].widget.attrs['wsize'] = '300'

    addPatientCaseForm.fields["medical_description"].widget.attrs['hgrp'] = '1'
    addPatientCaseForm.fields["medical_description"].widget.attrs['wsize'] = '600'

    addPatientCaseForm.fields["medical_history"].widget.attrs['hgrp'] = '1'
    addPatientCaseForm.fields["medical_history"].widget.attrs['wsize'] = '600'


    return render(request, 'main/patientcaseform.html', {'otherVars':otherVars,'addPatientCaseForm':addPatientCaseForm,'hgrps':hgrps})

@login_active_required(login_url=reverse_lazy('login'))
def issueDictionary(request):
    otherVars = {'pageType': 'logon', 'UserInfo': request.user.first_name}
    # if request method is post
    if request.method == 'POST':
        issueForm = IssueDictonaryForm(request.POST)
        # input validation for add user and user profile form
        if issueForm.is_valid():
            issue = str(request.POST['medicalTerm']).lower()
            list_dict = issueinformation(issue)
            if not list_dict ==[]:
                d = ''
                for dic in list_dict:
                    d += dic + '\n'
            else:
                d = 'Cannot find definition'
            issueForm = IssueDictonaryForm(initial={
                'medicalTerm':issue,
                'description':'Definition: ' + '\n' + '\n' + d})
        else:
            pass


    else:
        issueForm = IssueDictonaryForm()



    hgrps = ({'name': 'Medical Dictionary', 'lblwidth': '160', 'value': '0'},)
    issueForm.fields["medicalTerm"].widget.attrs['hgrp'] = '0'
    issueForm.fields["medicalTerm"].widget.attrs['wsize'] = '300'

    issueForm.fields["description"].widget.attrs['hgrp'] = '0'
    issueForm.fields["description"].widget.attrs['wsize'] = '600'

    return render(request, 'main/medicaldictionary.html', {'otherVars':otherVars,'issueForm':issueForm,'hgrps':hgrps})
