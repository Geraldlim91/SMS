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





   # if bool(illness1) == False:

