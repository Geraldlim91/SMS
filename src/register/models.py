from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator

class User_Profile(models.Model):

    user = models.ForeignKey(User, primary_key=True, unique=True)
    contact_num = models.CharField(max_length=10)
    class Meta:
        db_table = "user"