from django.db import models
from acc.models import User
from django.utils import timezone

# Create your models here.


class Board(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.CharField(max_length=30)
    content = models.TextField()
    likey = models.IntegerField(default=0)
    up = models.ManyToManyField(User)
    c_time = models.DateTimeField()

    def __str__(self):
        return self.subject


class Reply(models.Model):
    subject = models.ForeignKey(Board, on_delete=models.CASCADE)
    replyer = models.CharField(max_length=100)
    comment = models.TextField()
    pic = models.ImageField()
