from django.db import models
from acc.models import User


class Quiz(models.Model):
    question = models.TextField()
    answer = models.TextField()
    solver = models.ManyToManyField(User, blank=True)
    point = models.IntegerField()
