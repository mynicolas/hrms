#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from control import *


class Log(models.Model):
    content = models.TextField()
    logTime = models.DateTimeField()
    user = models.ForeignKey(User)


class LogRequest(object):
    def __init__(self, user):
        self.user = user
        self.count = 20
        self.content = []
        _contentObjs = self.user.log_set.all()
        _datetime = datetime2String
        if _contentObjs:
            for aContentO in _contentObjs:
                content = ''
                datetime = datetime2String(aContentO.logTime)
                content = "%s/%s/%s-%s:%s:%s  %s  %s" %\
                    (datetime['month'], )


