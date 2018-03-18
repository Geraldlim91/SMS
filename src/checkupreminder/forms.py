from django import forms
from django.contrib.auth.models import User
import re


class reminderForm(forms.Form):
    OPTIONS = (
        ("checkup1", "Full body health screening"),
        ("checkup2", "Lung Cancer screening"),
        ("checkup3", "Brain Cancer screening"),
    )
    screenings = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)

    #illness1= forms.BooleanField(widget=forms.CheckboxInput,label="Full body health screening")
   # illness2 = forms.BooleanField(widget=forms.CheckboxInput,label="Lung Cancer screening")

    #if illness1 == False and illness2 == False:
     #   raise forms.ValidationError("You have not selected any illness!")


class addScreeningForm(forms.Form):
    screeningname = forms.CharField(max_length=32, label="Screening Name")
    age_grp = forms.CharField(max_length=100, label="Age Group")
    gender = forms.CharField(max_length=20, label="Gender")
    description = forms.CharField(max_length=20, label="Description")
    message = forms.CharField(max_length=20, label="Reminder message")

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



   # if bool(illness1) == False:

