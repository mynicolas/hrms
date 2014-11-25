#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from HRMSApp.models import Company


class Profile(models.Model):
    question = models.CharField(max_length=128, null=True, default='')
    answer = models.CharField(max_length=128, null=True, default='')
    weixin = models.CharField(max_length=32)
    phone = models.CharField(max_length=16)
    instanceSort = models.TextField()
    user = models.ForeignKey(User, unique=True)
    company = models.ForeignKey(Company)


class Permission(models.Model):
    isSuperuser = models.BooleanField()   # 是否为管理员
    isLocked = models.BooleanField()  # 是否为新成员
    isDeleted = models.BooleanField()     # 是否为网站成员
    queryPermission = models.TextField()    # 对instance的某些信息的查询权限
    modify_permission = models.TextField()  # 对instance的某些信息的修改权限
    user = models.ForeignKey(User, unique=True)
