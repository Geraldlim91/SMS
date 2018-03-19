from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import registerForm
from models import User_Profile
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    otherVars = {'pageType':'register'}
    # if request method is post
    if request.method == 'POST':
        regForm = registerForm(request.POST)
        userIns = User()
        userIns.email = request.POST['email']
        userIns.username = request.POST['email']
        userIns.set_password(request.POST['password'])
        userIns.first_name = request.POST['first_name']
        userIns.last_name = request.POST['last_name']
        try:
            userIns.save()
        except:
            return HttpResponseRedirect(reverse('register'))

        userIns2 = User_Profile()
        userIns2.user_id = userIns.id
        userIns2.contact_num = request.POST['contact_num']

        userIns2.save()
        return HttpResponseRedirect(reverse('login'))
    else:
        regForm = registerForm()

    # Define header groups
    hgrps = ({'name':'Sign Up Information','lblwidth':'160'}, {'name':'Personal Information','lblwidth':'160'},)
    # For first header group
    regForm.fields["email"].widget.attrs['hgrp'] = '0'
    regForm.fields["email"].widget.attrs['wsize'] = '300'

    regForm.fields["password"].widget.attrs['hgrp'] = '0'
    regForm.fields["password"].widget.attrs['wsize'] = '300'

    regForm.fields["confirm_password"].widget.attrs['hgrp'] = '0'
    regForm.fields["confirm_password"].widget.attrs['wsize'] = '300'

    # For first header group
    regForm.fields["first_name"].widget.attrs['hgrp'] = '1'
    regForm.fields["first_name"].widget.attrs['wsize'] = '300'

    regForm.fields["last_name"].widget.attrs['hgrp'] = '1'
    regForm.fields["last_name"].widget.attrs['wsize'] = '300'

    regForm.fields["contact_num"].widget.attrs['hgrp'] = '1'
    regForm.fields["contact_num"].widget.attrs['wsize'] = '300'
    regForm.fields["contact_num"].label = 'Contact number'


    return render(request, 'main/register.html', {'otherVars':otherVars,'regForm':regForm,'hgrps':hgrps,})