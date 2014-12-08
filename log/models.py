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
    def __init__(self, user):
        self.user = user
        self.content = []
        self.__create()

    def __create(self):
        _contentObjs = self.user.log_set.all()
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
            self.content.reverse()
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

    def get(
            self,
            host='',
            count=20,
            multiple=1,
            startTime=None,
            endTime=None
            ):
        """
        获取日志
        host: 需要查询的实例名
        count: 每页的日志条目数
        multiple: 日志页数（每页 = self.count条），如果为 0 ，则获取所有日志
        startTime: 需要查询的日志开始日期
        endTime: 需要查询的日志结束日期
        """
        if not multiple:
            _contentObjs = None
            logs = self.content
            return logs
        elif not host and not startTime and not endTime and multiple:
            _contentObjs = None
            logs = self.content
            if len(logs) >= count * multiple:
                logs = logs[0:count * multiple]
            else:
                logs = logs[0:]
            return logs
        elif startTime and endTime:
            _contentObjs = self.user.log_set.filter(
                logTime__range=(startTime, endTime),
                content__icontains=host
                )
        elif not startTime and not endTime and host:
            _contentObjs = self.user.log_set.filter(
                content__icontains=host
                )
        else:
            return ['query error']

        if _contentObjs:
            logs = []
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
                logs.append(_content)
            logs.reverse()
        else:
            logs = ['There is no log.']

        return logs
