#!/usr/bin/env python
#-*- coding: utf-8 -*-


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
