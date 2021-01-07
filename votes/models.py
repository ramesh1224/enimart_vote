from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ManyToManyField(Region, null=True, blank=True)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    question = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
