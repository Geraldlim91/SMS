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
from src.login.decorator import login_active_required
from models import Patient, Patient_Record

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
            str(patientObj.dob),
        ])
    tableInfo = {'patientList': json.dumps(patientList), 'numOfRecords': numOfRecords}

    if len(patientList) > 0:
        tableInfo['recordStart'] = 1
        tableInfo['recordEnd'] = len(patientList)
    if numOfRecords > 10:
        tableInfo['nextEnabled'] = 'Y'

    filterVars = [{'name': 'Active', 'column': '7', 'text': ['Yes', 'No'], 'value': ['1', '0']},
                  {'name': 'Staff', 'column': '8', 'text': ['Yes', 'No'], 'value': ['1', '0']}]

    # Message to display when delete is pressed (<title>,<body>)
    delMsg = ('Delete user(s)?', 'user(s) will be permanently deleted and cannot be recovered. \
              You can consider inactivating the accounts instead. Are you sure you want to proceed to delete the users?')

    # Message to display when table has no records
    tabEmptyMsg = 'No user accounts available for viewing'
    return render(request, 'main/patientview.html', {'otherVars': otherVars, 'tableInfo': tableInfo, 'filterVars': json.dumps(filterVars), 'delMsg': delMsg, 'tabEmptyMsg': tabEmptyMsg})


# @login_active_required(login_url=reverse_lazy('login'))
# def userViewUpdate(request):
#     if request.user.has_perm("profile.custom_view_users"):
#         if request.method == 'POST':
#             sortingNames = ['id', 'username', 'first_name', 'last_name', 'email',
#                             'groups__name', 'is_active', 'is_staff', 'is_superuser',
#                             'date_joined',
#                             # 'profile__country__iso'
#             ]
#             sortOrder = []
#             for val in json.loads(request.POST['sortingType']):
#                 sortOrder.append(('-' if val['order'] == 1 else '') + sortingNames[val['value']])
#
#             query = Q()
#             if 'searchText' in request.POST:
#                 searchText = json.loads(request.POST['searchText'])
#                 tSearchArr = []
#                 fInputArr = []
#                 for sItem in searchText:
#                     if sItem['searchType'] == 'sText':
#                         tSearchArr = [('username__icontains', sItem['searchTerm']),
#                                       ('first_name__icontains', sItem['searchTerm']),
#                                       ('last_name__icontains', sItem['searchTerm']),
#                                       ('email__icontains', sItem['searchTerm']),
#                                       ('groups__name__icontains', sItem['searchTerm'])]
#
#                         if isInt(sItem['searchTerm']):
#                             tSearchArr.append(('id', int(sItem['searchTerm'])))
#
#                     elif sItem['searchType'] == '7':
#                         fInputArr.append(('is_active', int(sItem['searchTerm'])))
#                     elif sItem['searchType'] == '8':
#                         fInputArr.append(('is_staff', int(sItem['searchTerm'])))
#                 for item in [Q(x) for x in tSearchArr]:
#                     query |= item
#                 for item in [Q(x) for x in fInputArr]:
#                     query &= item
#
#             if query:
#                 numOfRecords = User.objects.filter(query).count()
#             else:
#                 numOfRecords = User.objects.count()
#
#             recordStart = int(request.POST['recordStart'])
#             recordEnd = int(request.POST['recordEnd'])
#             pageLength = int(request.POST['pageLength'])
#
#             if 'paginate' in request.POST:
#                 paginate = request.POST['paginate']
#                 if paginate == 'next':
#                     recordStart = recordEnd + 1
#                 elif paginate == 'prev':
#                     recordStart -= pageLength
#                 elif paginate == 'first':
#                     recordStart = 1
#                 elif paginate == 'last':
#                     recordStart = numOfRecords - pageLength + 1
#             if recordStart > numOfRecords:
#                 recordStart = numOfRecords
#             if recordStart < 1 or 'firstSearch' in request.POST:
#                 recordStart = 1
#             if query:
#                 # profileObjects = User_Profile.objects.filter(query).order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]
#                 userObjects = User.objects.filter(query).order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]
#             else:
#                 # profileObjects = User_Profile.objects.all().order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]
#                 userObjects = User.objects.all().order_by(*sortOrder)[recordStart - 1:recordStart + pageLength - 1]
#
#             listLength = len(userObjects)
#             userList = []
#             for userObj in userObjects:
#                 try:
#                     profObj = userObj.get_profile()
#                 except (Exception):
#                     profObj = None
#                 userList.append([
#                     str(userObj.id),
#                     userObj.username,
#                     userObj.first_name,
#                     userObj.last_name,
#                     userObj.email,
#                     ','.join(userObj.groups.values_list('name', flat=True)),
#                     getSign(userObj.is_active,'userActive', userObj.id),
#                     (okSign if userObj.is_staff else errorSign),
#                     (okSign if userObj.is_superuser else errorSign),
#                     djangoDate(localtime(userObj.date_joined)),
#                     str(profObj.country.iso) if profObj is not None else '-'
#                 ])
#
#             tableInfo = {'valueList': userList, 'numOfRecords': numOfRecords}
#             if listLength > 0:
#                 recordEnd = recordStart + listLength - 1
#                 if recordStart > 1:
#                     tableInfo['prevEnabled'] = 'Y'
#                 if recordEnd < numOfRecords:
#                     tableInfo['nextEnabled'] = 'Y'
#             else:
#                 recordStart = 0
#                 recordEnd = 0
#             tableInfo['recordStart'] = recordStart
#             tableInfo['recordEnd'] = recordEnd
#             return HttpResponse(json.dumps(tableInfo))
#         else:
#             return HttpResponseRedirect(reverse('userView'))
#     else:
#         return HttpResponseRedirect(reverse('a_index'))