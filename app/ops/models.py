# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class server(models.Model):
    hostname=models.CharField(max_length=50)
    band=models.CharField(max_length=100)
    raid=models.CharField(max_length=50)
    disk=models.CharField(max_length=50)
    memory=models.CharField(max_length=15)
    cpu=models.CharField(max_length=50)
    in_out=models.CharField(max_length=80)
    in_in=models.CharField(max_length=80)
    os=models.CharField(max_length=50)
    sn=models.CharField(max_length=100)
    idc=models.CharField(max_length=100)

class inventory(models.Model):
    host=models.CharField(max_length=50)

#class d_category(models.Model):
#    category=models.CharField(max_length=100)
#
#class docs(models.Model):
#    title=models.CharField(max_length=200)
#    category=models.CharField(max_length=100)
#    author=models.CharField(max_length=50)
#    date=models.DateField()
#    text=models.TextField()
    
