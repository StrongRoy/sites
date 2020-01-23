from django.conf import settings
from django.urls import reverse
from django.db import models


# Create your models here.
class List(models.Model):
    text = models.IntegerField(default=0)

class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List,default=None,on_delete=models.CASCADE)
