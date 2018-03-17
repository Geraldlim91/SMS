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
    contact_num = forms.CharField(max_length=8, label="Contact Number")
    full_name = forms.CharField(max_length=100, label="Full Name")
    gender = forms.CharField(max_length=20, label="Gender")
    dob = forms.DateField(label="Date of Birth", input_formats=DATE_INPUT_FORMATS)
    address = forms.CharField(max_length=200)
    postalcode = forms.CharField(max_length=10, label="Postal Code")
    nok = forms.CharField(max_length=100, label="Next-of-Kin")
    email = forms.CharField(max_length=50)
    allergy = forms.CharField(max_length=100)

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


# change user form
# class ChangeUserForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         hgrps = kwargs.pop('hgrps', None)
#         super(ChangeUserForm, self).__init__(*args, **kwargs)
#         if user is None or user.is_superuser == 0:
#             del self.fields['is_superuser']
#         GROUP_CHOICES = [(x.id, x.name) for x in Group.objects.all()]
#         self.fields.update({'groups': forms.CharField(widget=forms.Select(choices=GROUP_CHOICES),
#                                                       help_text=" The role the user belongs in. Permissions of the user will be based on the role assigned")})
#
#         if hgrps is not None:
#             for val in hgrps:
#                 for key, item in self.fields.iteritems():
#                     # For first header group
#                     if val['name'] == 'Change User' and key in ['username']:
#                         item.widget.attrs['hgrp'] = '0'
#
#                     # For second header group
#                     elif val['name'] == 'Personal Information' and key in ['first_name', 'last_name', 'email']:
#                         item.widget.attrs['hgrp'] = '1'
#                         if key == 'email':
#                             item.widget.attrs['wsize'] = '300'
#
#                     # For third header group
#                     elif val['name'] == 'Permissions' and key in ['is_superuser', 'is_staff', 'is_active', 'groups']:
#                         item.widget.attrs['hgrp'] = '2'
#                         if key == 'groups':
#                             item.widget.attrs['wsize'] = '500'
#
#     class Meta:
#         model = Patient
#         exclude = ('last_login', 'date_joined', 'user_permissions', 'password', 'groups')
#
#     def clean_first_name(self):
#         first_name = self.cleaned_data.get('first_name', '')
#
#         if len(first_name) == 0:
#             raise forms.ValidationError("This field is required.")
#
#         return first_name
#
#     def clean_last_name(self):
#         last_name = self.cleaned_data.get('last_name', '')
#
#         if len(last_name) == 0:
#             raise forms.ValidationError("This field is required.")
#
#         return last_name
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email', '')
#
#         if len(email) == 0:
#             raise forms.ValidationError("This field is required.")
#         if re.search("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$", email, re.IGNORECASE) is None:
#             raise forms.ValidationError("Email address is invalid")
#
#         return email
#
#
# # add user profile form
# class AddProfileForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         hgrps = kwargs.pop('hgrps', None)
#         super(AddProfileForm, self).__init__(*args, **kwargs)
#
#         if hgrps is not None:
#             for val in hgrps:
#                 for key, item in self.fields.iteritems():
#                     # For second header group
#                     if val['name'] == 'Personal Information' and key in ['country', 'phone_number']:
#                         item.widget.attrs['hgrp'] = '1'
#                         if key == 'country':
#                             item.widget.attrs['wsize'] = '340'
#
#     class Meta:
#         model = User_Profile
#         exclude = ('user', 'verification_code')
#
#     def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number', '')
#
#         if len(phone_number) == 0:
#             raise forms.ValidationError("This field is required.")
#
#         return phone_number
#
#
# # Update user information form
# class UpdateUserInfoForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         hgrps = kwargs.pop('hgrps', None)
#         super(UpdateUserInfoForm, self).__init__(*args, **kwargs)
#
#         if hgrps is not None:
#             for val in hgrps:
#                 for key, item in self.fields.iteritems():
#                     # For first header group
#                     if val['name'] == 'Update Personal Information' and key in ['first_name', 'last_name', 'email']:
#                         item.widget.attrs['hgrp'] = '0'
#                         if key == 'email':
#                             item.widget.attrs['wsize'] = '300'
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')
#
#     def clean_first_name(self):
#         first_name = self.cleaned_data.get('first_name', '')
#
#         if len(first_name) == 0:
#             raise forms.ValidationError("This field is required.")
#
#         return first_name
#
#     def clean_last_name(self):
#         last_name = self.cleaned_data.get('last_name', '')
#
#         if len(last_name) == 0:
#             raise forms.ValidationError("This field is required.")
#
#         return last_name
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email', '')
#
#         if len(email) == 0:
#             raise forms.ValidationError("This field is required.")
#         if re.search("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$", email, re.IGNORECASE) is None:
#             raise forms.ValidationError("Email address is invalid")
#
#         return email
#
#
# # Update user profile form
# class UpdateUserProfileForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         hgrps = kwargs.pop('hgrps', None)
#         super(UpdateUserProfileForm, self).__init__(*args, **kwargs)
#
#         self.fields.update({'exist_avatar': forms.CharField(widget=ImageDisplay(), label="Existing Avatar", help_text=" Existing avatar image", required=False),
#                             'avatar_img': forms.FileField(label="Upload New Avatar", help_text=" Upload new avatar image", required=False)})
#         self.fields.keyOrder = ['country', 'phone_number', 'exist_avatar', 'avatar_img']
#
#         if hgrps is not None:
#             for val in hgrps:
#                 for key, item in self.fields.iteritems():
#                     # For first header group
#                     if val['name'] == 'Update Personal Information' and key in ['country', 'phone_number', 'exist_avatar', 'avatar_img']:
#                         item.widget.attrs['hgrp'] = '0'
#                         if key == 'country':
#                             item.widget.attrs['wsize'] = '340'
#
#     class Meta:
#         model = User_Profile
#         exclude = ('user', 'verification_code')
#
#     def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number', '')
#
#         if len(phone_number) == 0:
#             raise forms.ValidationError("This field is required.")
#
#         return phone_number
#
#     def clean_avatar_img(self):
#         image = self.cleaned_data.get('avatar_img', False)
#         ext_whitelist = ['.gif', '.png', '.jpg', '.jpeg']
#         if image:
#             if image._size > 4*1024*1024:
#                 raise forms.ValidationError("Image file too large ( > 4mb )")
#             filename = image.name
#             if not re.match(r'[a-z0-9_\- .]+$', filename, re.IGNORECASE):
#                 raise forms.ValidationError("Invalid characters in filename! (Allowed: a-z, A-Z, 0-9, _, -, periods and spaces)")
#             ext = os.path.splitext(filename)[1]
#             ext = ext.lower()
#             if ext not in ext_whitelist:
#                 raise forms.ValidationError("Filetype is not allowed!")
#             return image
#
#
# # change password form
# class ChangePasswordForm(forms.Form):
#
#     oldPwd = forms.CharField(label="Old password", widget=forms.PasswordInput, help_text="Value of old password use to login")
#     newPwd = forms.CharField(label="New password", widget=forms.PasswordInput, help_text="Password must contain 1 uppercase, 1 lowercase and 1 numeric digit")
#     cfmPwd = forms.CharField(label="Confirm password", widget=forms.PasswordInput, help_text="Retype the password")
#
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         hgrps = kwargs.pop('hgrps', None)
#         super(ChangePasswordForm, self).__init__(*args, **kwargs)
#
#         if hgrps is not None:
#             for val in hgrps:
#                 for key, item in self.fields.iteritems():
#                     # For first header group
#                     if val['name'] == 'Change Password' and key in ['oldPwd', 'newPwd', 'cfmPwd']:
#                         item.widget.attrs['hgrp'] = '0'
#
#     def clean_oldPwd(self):
#         oldPwd = self.cleaned_data.get('oldPwd', '')
#         if not self.user.check_password(oldPwd):
#             raise forms.ValidationError("Old password does not match")
#         return oldPwd
#
#     def clean_newPwd(self):
#         oldPwd = self.cleaned_data.get('oldPwd', '')
#         newPwd = self.cleaned_data.get('newPwd', '')
#
#         if len(newPwd) < 8:
#             raise forms.ValidationError("Length of password must be at least 8 characters")
#         if re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,%d}$" % int(len(newPwd)), newPwd) is None:
#             raise forms.ValidationError("Password must contain 1 uppercase, 1 lowercase and 1 numeric digit")
#         if newPwd == oldPwd:
#             raise forms.ValidationError("Old and new password must not be the same")
#         return newPwd
#
#     def clean_cfmPwd(self):
#         newPwd = self.cleaned_data.get('newPwd')
#         cfmPwd = self.cleaned_data.get('cfmPwd')
#         if newPwd and cfmPwd:
#             if newPwd != cfmPwd:
#                 raise forms.ValidationError("Sorry, passwords do not match")
#
#         return cfmPwd
#
#     def save(self, commit=True):
#         self.user.set_password(self.cleaned_data["newPwd"])
#         if commit:
#             self.user.save()
#         return self.user
#
#
# class AddGroupForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         hgrps = kwargs.pop('hgrps', None)
#         super(AddGroupForm, self).__init__(*args, **kwargs)
#
#         PER_CHOICES = [(x.id, x.name) for x in Permission.objects.filter(name__contains='|')]
#
#         self.fields.update({'permissions': forms.CharField(widget=forms.SelectMultiple(choices=PER_CHOICES),
#                                                            label="Privileges",
#                                                            help_text="Select the privileges that will be granted to this role. Hold control (Command on mac) to choose more than 1")})
#
#         if hgrps is not None:
#             for val in hgrps:
#                 for key, item in self.fields.iteritems():
#                     # For first header group
#                     if val['name'] in ['Add Role','Change Role'] and key in ['name']:
#                         item.widget.attrs['hgrp'] = '0'
#                         item.help_text = "Name of the role that will be added"
#                     # For second header group
#                     elif val['name'] == 'Role Privileges' and key in ['permissions']:
#                         item.widget.attrs['hgrp'] = '1'
#
#     class Meta:
#         model = Group
#         fields = ('name',)
#
#
# class TransferDeviceForm(ModelForm):
#     def __init__(self, request, *args, **kwargs):
#         self.request = request
#         hgrps = kwargs.pop('hgrps', None)
#         super(TransferDeviceForm, self).__init__(*args, **kwargs)
#
#         USER_CHOICES = [(x.username, x.username) for x in User.objects.all().exclude(username=self.request.user.username)]
#
#         self.fields.update({'user': forms.CharField(widget=forms.Select(choices=USER_CHOICES),
#                                                     help_text="Available users in the system")})
#
#         if hgrps is not None:
#             for key, item in self.fields.iteritems():
#                 # For first header group
#                 if key in ['user']:
#                     item.widget.attrs['hgrp'] = '0'
#                     item.widget.attrs['wsize'] = '250'
#
#     class Meta:
#         model = User
#         fields = ()
#
#     def clean_user(self):
#         new_user = self.cleaned_data.get('user', '')
#
#         if new_user == self.request.user.username:
#             raise forms.ValidationError("You cannot transfer to yourself. Please choose a different user.")
#
#         return new_user