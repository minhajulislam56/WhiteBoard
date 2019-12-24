from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_unicode_slug
import uuid
from django.conf import settings

def gen_profile_pic(instance, filename):
    return "ProfilePic/{username}/{filename}".format(username=instance.username, filename=filename)

class User(AbstractUser):
    GENDER_CHOICE = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True, blank=False, validators=[validate_unicode_slug])
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=200, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, blank=False)
    email_verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=300)
    signup_time = models.DateTimeField(auto_now_add=True)
    login_time = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(upload_to=gen_profile_pic, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


