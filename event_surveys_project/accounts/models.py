from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_superadmin = models.BooleanField(default=False)
    

# Create your models here.
