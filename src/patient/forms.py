import re
import os
from src.config import DATE_INPUT_FORMATS
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission

from models import Patient, Patient_Record



# add user form
class AddPatientForm(forms.Form):
    nric = forms.CharField(max_length=32, label="NRIC")
    full_name = forms.CharField(max_length=100, label="Full Name")
    contact_num = forms.CharField(max_length=8, label="Contact Number")
    gender = forms.CharField(max_length=20, label="Gender")
    dob = forms.DateField(label="Date of Birth", help_text="Format in YYYY-MM-DD")
    address = forms.CharField(max_length=200)
    postalcode = forms.CharField(max_length=10, label="Postal Code")
    nok = forms.CharField(max_length=100, label="Next-of-Kin")
    email = forms.CharField(max_length=50)
    allergy = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        hgrps = kwargs.pop('hgrps', None)
        super(AddPatientForm, self).__init__(*args, **kwargs)
        # For first header group
        if hgrps is not None:
            for val in hgrps:
                for key, item in self.fields.iteritems():
                    # For first header group
                    if val['name'] in ['Add Mobile Device', 'Edit Mobile Device']:
                        item.widget.attrs['hgrp'] = '0'
                        if key == 'active':
                            item.widget.attrs['switch'] = ''
    class Meta:
        model = Patient

        # exclude = ('last_login', 'date_joined', 'user_permissions', 'password', 'groups')

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
    
        if len(email) == 0:
            raise forms.ValidationError("This field is required.")
        if re.search("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$", email, re.IGNORECASE) is None:
            raise forms.ValidationError("Email address is invalid")
    
        return email

