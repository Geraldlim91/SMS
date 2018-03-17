from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import registerForm
from models import User_Profile
# Create your views here.

def register(request):
    otherVars = {'pageType':'register'}
    # if request method is post
    if request.method == 'POST':
        regForm = registerForm(request.POST)

        # input validation for add user and user profile form
        if regForm.is_valid():
            # save the user and user profile object into database
            userIns = User_Profile()
            userIns.email = request.POST['email']
            userIns.username = userIns.email
            userIns.set_password(request.POST['password'])
            userIns.first_name = request.POST['first_name']
            userIns.last_name = request.POST['last_name']
            if userIns.contact_num == None:
                userIns.contact_num = 'N.A'
            else:
                userIns.contact_num = request.POST['contact_num']

            userIns.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            pass
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


    return render(request, 'main/register.html', {'otherVars':otherVars,'regForm':regForm,'hgrps':hgrps})