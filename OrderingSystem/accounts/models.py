from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^[+|\d][0-9() -]*\d$', message="Please enter a correct phone number.")
    phone = models.CharField('Phone Number', validators=[phone_regex], null=True, blank=True, max_length=20)
    image = models.FileField('Profile Picture', upload_to='customer/%Y/%m/%d', null=True, blank=True)

    objects = UserManager()
