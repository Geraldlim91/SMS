import re
import os
from src.config import DATE_INPUT_FORMATS
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission

from models import Patient, Patient_Record


class AddPatientCaseForm(forms.Form):
    nric = forms.CharField(max_length=32, label="NRIC")
    medical_description =  forms.CharField(label="Medical Description",widget=forms.Textarea, required=False)
    medical_history = forms.CharField(label="Medical History",widget=forms.Textarea, required=False)
    symptoms = forms.CharField(label="Symptoms")
    diagnosis = forms.CharField(label="Diagnosis",widget=forms.Textarea, required=False)

    class Meta:
        model = Patient_Record

GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

# add user form
class AddPatientForm(forms.Form):
    nric = forms.CharField(max_length=32, label="NRIC")
    full_name = forms.CharField(max_length=100, label="Full Name")
    contact_num = forms.CharField(max_length=8, label="Contact Number")
    gender = forms.CharField(label="Gender", widget=forms.Select(choices=GENDER))
    dob = forms.DateField(label="Date of Birth", help_text="Format in YYYY-MM-DD",widget=forms.DateInput)
    address = forms.CharField(max_length=200)
    postalcode = forms.CharField(max_length=10, label="Postal Code")
    nok = forms.CharField(max_length=100, label="Next-of-Kin")
    email = forms.CharField(max_length=50)
    allergy = forms.CharField(max_length=100,help_text="No allergy, enter Nil")

    class Meta:
        model = Patient



    def clean_email(self):
        email = self.cleaned_data.get('email', '')
    
        if len(email) == 0:
            raise forms.ValidationError("This field is required.")
        if re.search("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$", email, re.IGNORECASE) is None:
            raise forms.ValidationError("Email address is invalid")
    
        return email

class IssueDictonaryForm(forms.Form):
    medicalTerm = forms.CharField(max_length=100, label="Medical Term")
    description = forms.CharField(label="Description", widget=forms.Textarea, required=False)