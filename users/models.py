from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUsers(AbstractUser):
   user_photo = models.ImageField(upload_to='users/', blank=True, null=True)# Create your models here.
