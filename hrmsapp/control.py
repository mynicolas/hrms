#!/usr/bin/env python
#-*- coding: utf-8 -*-
from userprofile.models import *
from models import *


def checkPerm(user, perm):
    """
    检测对某个字段修改的权限
    param: user: 需要检测的用户
    param: perm: 需要检测的权限字符串
    return: boolean
    """
    permOs = user.perm_set.all()
    if permOs:
        modify = permOs[0].modify
        return perm in modify
    else:
        return False


def getVms(start=0, end=None, user=None):
    """
    获取指定范围的实例名列表
    param: start: 范围开始索引值，end: 范围结束的索引值
    return: list(instances)
    """
    vms = []
    if not user:
        user = User.objects.get(username='admin')
        sort = user.perm_set.all()
        if sort and sort[0].sort:
            vms = sort[0].sort.split(',')
            return vms
        else:
            instanceOs = Instance.objects.all()
    else:
        sort = user.perm_set.all()
        if sort and sort[0].sort:
            vms = sort[0].sort.split(',')
            return vms
        else:
            instanceOs = user.instance_set.all()

    if instanceOs:
        for i in instanceOs[start:end]:
            vms.append(i.instanceName)
    return vms

def addVmName(user, vmName):
    """
    添加实例的时候向sort中追加一个instanceName
    param:  user: 该登陆用户
            vmName: 需要追加的instanceName
    return: None
    """
    thisPerm = user.perm_set.all()[0]
    if thisPerm.sort:
        thisPerm.sort += ',%s' % vmName
    else:
        thisPerm.sort = None
    thisPerm.save()
