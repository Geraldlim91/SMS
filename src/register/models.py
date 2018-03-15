from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator

class User_Profile(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, unique=True)
    class Meta:
        db_table = "user"