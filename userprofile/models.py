#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from HRMSApp.models import Company

class Profile(models.Model):
    question = models.CharField(max_length = 128, null = True, default = '')
    answer = models.CharField(max_length = 128, null = True, default = '')
    weixin = models.CharField(max_length = 32)
    phone = models.CharField(max_length = 16)
    instanceSort = models.TextField()
    user = models.ForeignKey(User, unique = True)
    company = models.ForeignKey(Company)


