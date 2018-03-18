from django import forms
from django.contrib.auth.models import User
from models import NotificationCriteria
import re


class reminderForm(forms.Form):
    OPTIONS = (
        ("checkup1", "Full body health screening"),
        ("checkup2", "Lung Cancer screening"),
        ("checkup3", "Brain Cancer screening"),
    )
    screenings = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS,required=True)

    #illness1= forms.BooleanField(widget=forms.CheckboxInput,label="Full body health screening")
   # illness2 = forms.BooleanField(widget=forms.CheckboxInput,label="Lung Cancer screening")

    #if illness1 == False and illness2 == False:
     #   raise forms.ValidationError("You have not selected any illness!")


class addScreeningForm(forms.Form):
    screening_name = forms.CharField(max_length=32, label="Screening Name")
    age_grp = forms.CharField(max_length=100, label="Age Group")
    gender = forms.CharField(max_length=20, label="Gender", required=False)
    description = forms.CharField(max_length=400, label="Description",widget=forms.Textarea)
    message = forms.CharField(max_length=400, label="Reminder message",widget=forms.Textarea)

    class Meta:
        model = NotificationCriteria
        # exclude = ('last_login', 'date_joined', 'user_permissions', 'password', 'groups')


