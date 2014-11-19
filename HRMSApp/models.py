from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    companyName = models.CharField(max_length = 16, null = False, default = 'company name')

class Instance(models.Model):
    instanceName = models.CharField(max_length = 5, null = False, default = 'instance name')
    vcpus = models.CharField(max_length = 4, null = False, default = '4')
    mem = models.CharField(max_length = 5, null = False, default = '16')
    dataDisk = models.CharField(max_length = 8, null = False, default = '1024')
    macAddress = models.CharField(max_length = 17, null = False, default = 'aa.bb.cc.dd.ee.ff')
    startDate = models.DateField()
    useInterval = models.IntegerField(max_length = 255, null = False, default = 365)
    bandwidth = models.CharField(max_length = 4, null = False, default = '1')
    remotePort = models.CharField(max_length = 8)
    ip = models.CharField(max_length = 15)
    dogSn = models.CharField(max_length = 20)
    dogPort = models.CharField(max_length = 7)
    company = models.ForeignKey(Company)

class Node(models.Model):
    nodeName = models.CharField(max_length = 15)
    instance = models.ForeignKey(Instance)

class Ip(models.Model):
    ipAddress = models.CharField(max_length = 15)
    isUsed = models.BooleanField(default = False, null = False)

class Log(models.Model):
    content = models.TextField()
    logTime = models.DateTimeField()
    user = models.ForeignKey(User)


