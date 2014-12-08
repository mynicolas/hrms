#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime


def datetime2String(datetimeObj):
    """
    将datetime对象转换为string对象
    """
    datetimeDict = {}
    datetimeDict['year'] = datetimeObj.year
    datetimeDict['month'] = datetimeObj.month
    datetimeDict['day'] = datetimeObj.day
    datetimeDict['hour'] = datetimeObj.hour
    datetimeDict['minute'] = datetimeObj.minute
    datetimeDict['second'] = datetimeObj.second
    return datetimeDict


def string2Date(dateString):
    """
    将字符串转换为datetime.date对象
    :param dateString: 需要转换的字符串
    :return: datetime.date对象
    """
    dateList = dateString.split('/')
    return datetime.date(int(dateList[2]), int(dateList[0]), int(dateList[1]))
