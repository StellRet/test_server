from django.db import models

class PsychoType(models.Model):
    name = models.CharField(max_length=40, primary_key=True)

class User(models.Model):
    name = models.CharField(max_length=40, primary_key=True)
    ptypes = models.ManyToManyField(PsychoType)
