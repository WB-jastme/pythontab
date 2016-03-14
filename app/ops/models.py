# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class server(models.Model):
    hostname=models.CharField(max_length=50)
    band=models.CharField(max_length=100)
    raid=models.CharField(max_length=50)
    disk=models.CharField(max_length=50)
    memory=models.CharField(max_length=15)
    disk=models.CharField(max_length=50)
    cpu=models.CharField(max_length=50)
    interface_out=models.CharField(max_length=80)
    interface_in=models.CharField(max_length=80)
    os=models.CharField(max_length=50)
    sn=models.CharField(max_length=100)
    fixed_assets_encoding=models.CharField(max_length=100)
    owner=models.CharField(max_length=100)
    time=models.CharField(max_length=80)

class passets(models.Model):
    serial_number=models.CharField(max_length=50)
    department=models.CharField(max_length=100)
    owner=models.CharField(max_length=50)
    assets_type=models.CharField(max_length=50)
    version=models.CharField(max_length=15)
    cpu=models.CharField(max_length=50)
    memory=models.CharField(max_length=50)
    ipaddress=models.CharField(max_length=80)
    macaddress=models.CharField(max_length=80)

#class d_category(models.Model):
#    category=models.CharField(max_length=100)
#
#class docs(models.Model):
#    title=models.CharField(max_length=200)
#    category=models.CharField(max_length=100)
#    author=models.CharField(max_length=50)
#    date=models.DateField()
#    text=models.TextField()
    
