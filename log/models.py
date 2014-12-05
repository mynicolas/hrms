#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from control import *


class Log(models.Model):
    content = models.TextField()
    logTime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)


class LogRequest(object):
    def __init__(self, user, count=20):
        self.user = user
        self.count = count
        self.content = []
        self.__create()

    def __create(self):
        _contentObjs = self.user.log_set.all()
        if len(_contentObjs) >= self.count:
            _contentObjs = _contentObjs[0:self.count]
        else:
            _contentObjs = _contentObjs[:]
        if _contentObjs:
            for aContentO in _contentObjs:
                _logContent = aContentO.content
                datetime = datetime2String(aContentO.logTime)
                _content = "%s/%s/%s-%s:%s:%s  %s  %s" % (
                    datetime['month'],
                    datetime['day'],
                    datetime['year'],
                    datetime['hour'],
                    datetime['minute'],
                    datetime['second'],
                    self.user.username,
                    _logContent
                )
                self.content.append(_content)
        else:
            self.content = ['This user has no log.']

    def save(self, content):
        """
        保存一条新日志
        content: 新日志的内容
        """
        try:
            self.user.log_set.create(content=content)
            self.user.save()
            self.__create()
            return self
        except:
            return self

    def get(self, multiple=1):
        """
        获取日志
        multiple: 日志页数（每页 = self.count条）
        """
        logs = self.content
        if len(logs) >= self.count * multiple:
            logs = logs[0:self.count * multiple - 1]
        else:
            logs = logs[0:]
        return logs
