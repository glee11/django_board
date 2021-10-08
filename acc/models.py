from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    userpic = models.ImageField(upload_to="usr/%y", blank=True)
    nickname = models.CharField(max_length=30, blank=True)
    comment = models.TextField(blank=True)
    point = models.IntegerField(default=0)
    pass
