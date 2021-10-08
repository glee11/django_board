from django.db import models
from acc.models import User

# Create your models here.


class Topic(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    writer_pic = models.ImageField()
    comment = models.TextField()
    voter = models.ManyToManyField(User, blank=True)
    c_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.subject


class Choice(models.Model):
    subject = models.ForeignKey(Topic, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="vote")
    name = models.CharField(max_length=100)
    cuser = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
