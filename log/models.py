#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    content = models.TextField()
    logTime = models.DateTimeField()
    user = models.ForeignKey(User)


# class GetLog(object):
#     """
#     获取指定用户的日志内容
#     param: users: 指定用户的列表
#     """
#     def __init__(self, users):
#         self.users = users

#     def logContent(self):
#         """
#         获取该用户或用户列表的所有日志内容
#         return: 所有日志内容的列表
#         """
#         for user in self.users:
#             logs = user.log_set.all()
#             username = user.username
#             for log in logs:
#                 logData = "%s-%s--%s--%s" %\
