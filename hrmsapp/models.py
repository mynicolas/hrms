#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    companyName = models.CharField(max_length=16, null=False, unique=True)


class NodeHost(models.Model):
    node = models.CharField(max_length=17, null=False, unique=True)


class Instance(models.Model):
    instanceName = models.CharField(max_length=10, null=False, unique=True)
    vcpus = models.CharField(max_length=10, null=False)
    mem = models.CharField(max_length=10, null=False)
    dataDisk = models.CharField(max_length=10, null=False)
    startTime = models.DateTimeField(default=datetime.datetime.now())
    useInterval = models.IntegerField(max_length=6, null=False, default=365)
    bandwidth = models.CharField(max_length=4, null=False)
    user = models.ForeignKey(User)
    nodeHost = models.ForeignKey(NodeHost)
    company = models.ForeignKey(Company)


class Ip(models.Model):
    ipAddress = models.IPAddressField(null=False, unique=True)
    instance = models.ForeignKey(Instance, null=True)


class Mac(models.Model):
    macAddress = models.CharField(max_length=17, null=False, unique=True)
    instance = models.ForeignKey(Instance, null=True)


class UsbPort(models.Model):
    port = models.CharField(max_length=20, null=False)
    nodeHost = models.ForeignKey(NodeHost)
    instance = models.ForeignKey(Instance, null=True)

    class Meta:
        unique_together = (("port", "nodeHost"),)


class DogSN(models.Model):
    sn = models.CharField(max_length=20, null=False, unique=True)
    port = models.ForeignKey(UsbPort)


def getVms(start=0, end=10):
    """
    获取指定范围的实例名列表
    param: start: 范围开始索引值，end: 范围结束的索引值
    return: list(instances)
    """
    vmS = []
    for i in Instance.objects.all()[start:end]:
        vmS.append(i.instanceName)
    return vmS


class Vm(objects):
    def __init__(self, vmName):
        self.instanceName = None
        self.vcpus = None
        self.mem = None
        self.dataDisk = None
        self.startTime = None
        self.useInterval = None
        self.bandwidth = None
        self.nodeHost = None
        self.company = None
        self.dogSn = {}
        self.dogPort = []
        self.owner = None
        self.existed = False

        try:
            thisInstance = Instance.objects.get(instanceName=vmName)
        except Instance.DoesNotExist:
            self.instanceName = vmName
            self.existed = False
        else:
            self.instanceName = vmName
            self.vcpus = thisInstance.vcpus
            self.mem = thisInstance.mem
            self.dataDisk = thisInstance.dataDisk
            self.startTime = thisInstance.startTime
            self.useInterval = thisInstance.useInterval
            self.bandwidth = thisInstance.bandwidth
            self.nodeHost = thisInstance.nodeHost.node
            self.company = thisInstance.company.companyName
            self.dogPort = []
            self.dogSn = {}
            self.owner = None
            self.existed = True

            usbPorts = thisInstance.usbport_set.all()
            for i in usbPorts:
                self.dogPort.append(i.port)
                for j in i.dogsn_set.all():
                    self.dogSn[i.port] = j.sn

    def update(
        self,
        vmName=None,
        vcpus=None,
        mem=None,
        dataDisk=None,
        startTime=None,
        useInterval=None,
        bandwidth=None,
        nodeHost=None,
        company=None,
        dogSn=None,
        dogPort=None,
        owner=None,
    ):
        # 如果该实例不存在，则创建新实例
        if not self.existed:
            self.__create(
                vmName=self.instanceName,
                vcpus=self.vcpus,
                mem=self.mem,
                dataDisk=self.dataDisk,
                startTime=self.startTime,
                useInterval=self.useInterval,
                bandwidth=self.bandwidth,
                nodeHost=self.nodeHost,
                company=self.company,
                dogSn=self.dogSn,
                dogPort=self.dogPort,
                dogPort=self.owner
            )

        # 如果该实例已存在，则修改该实例的相关信息
        if not self.instanceName:
            self.instanceName = vmName
            thisInstance = Instance.objects.get(instanceName=self.instanceName)
            thisInstance.instanceName = self.instanceName
            thisInstance.save()

        thisInstance = Instance.objects.get(instanceName=self.instanceName)

        if not mem:
            thisInstance.mem = mem

        if not mem:
            thisInstance.dataDisk = dataDisk

        if not dataDisk:
            thisInstance.dataDisk = dataDisk

        if not startTime:
            thisInstance.startTime = startTime

        if not useInterval:
            thisInstance.useInterval = useInterval

        if not bandwidth:
            thisInstance.bandwidth = bandwidth

        if not nodeHost:
            thisInstance.nodeHost = NodeHost.objects.get(node=nodeHost)

        if not company:
            thisInstance.company = Company.objects.get(companName=company)
        thisInstance.save()

    def __create(
        self,
        vmName=None,
        vcpus=None,
        mem=None,
        dataDisk=None,
        startTime=None,
        useInterval=None,
        bandwidth=None,
        nodeHost=None,
        company=None,
        dogSn=None,
        dogPort=None,
        owner=None,
    ):
        """
        创建一个新的instance, 判断ip, mac, dogPort是否已经被使用
        params: vmName: 实例名
                vcpus: cpu个数
                mem: 内存
                dataDisk: 磁盘
                startTime: 开始时间
                useInterval: 使用期限
                bandwidth: 贷款
                nodeHost: 节点
                company: 公司名
                dogSn: 狗号
                dogPort: 狗
                owner: 拥有者
        return: boolean
        """
        try:
            
        return True
