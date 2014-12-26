#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    companyName = models.CharField(max_length=16, null=True, unique=True)


class NodeHost(models.Model):
    node = models.CharField(max_length=17, null=False, unique=True)


class BusinessMan(models.Model):
    name = models.CharField(max_length=10)


class Instance(models.Model):
    instanceName = models.CharField(max_length=10, null=False, unique=True)
    vcpus = models.CharField(max_length=10, null=False)
    mem = models.CharField(max_length=10, null=False)
    dataDisk = models.CharField(max_length=10, null=False)
    startTime = models.DateTimeField(null=False)
    useInterval = models.IntegerField(max_length=6, null=False, default=365)
    bandwidth = models.CharField(max_length=4, null=True)
    user = models.ForeignKey(User, null=False)
    nodeHost = models.ForeignKey(NodeHost, null=False)
    company = models.ForeignKey(Company, null=True)
    businessMan = models.ForeignKey(BusinessMan, null=True)


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
    port = models.OneToOneField(UsbPort, null=False)


def date2String(date):
    """
    将日期对象转换为字符串
    :param date: 需要转换成字符串的date对象
    :return: 日期字符串
    """
    return "%s/%s/%s" % (date.month, date.day, date.year)


def days2DateString(then, days):
    """
    将日期对象和具体的天数days相加得到最终的日期
    :param then: datetime.date对象
    :param days: 整型天数
    :return:最终的日期string
    """
    overtime = then + datetime.timedelta(days)
    return "%s/%s/%s" % (overtime.month, overtime.day, overtime.year)


def date2Days(start, end):
    """
    将日期间隔转换为天数
    :param start: 开始日期string
    :param end:  结束日期string
    :return: int，天数
    """
    dayDelta = (end - start).days
    return dayDelta


def string2Date(dateString):
    """
    将字符串转换为datetime.date对象
    :param dateString: 需要转换的字符串
    :return: datetime.date对象
    """
    dateList = dateString.split('/')
    return datetime.date(
        int(dateList[2]),
        int(dateList[0]),
        int(dateList[1])
    )


class Vm(object):
    """
    创建或者更新一个instance
    """
    def __init__(self, vmName):
        self.instanceName = vmName
        self.vcpus = None
        self.mem = None
        self.dataDisk = None
        self.startTime = None
        self.useInterval = None
        self.bandwidth = None
        self.nodeHost = None
        self.company = None
        #{'2-1.5': 'xxx', '2-1.6': 'xxx', ...}
        self.dogSn = {}
        #['2-1.5', '2-1.6', ...]
        self.dogPort = []
        #格式:['192.168.1.1', '192.168.1.1', ...]
        self.ip = []
        #格式:['52:54:00:00:00:00', '52:54:00:00:00:01', ...]
        self.mac = []
        self.owner = None
        self.businessMan = None
        self.existed = False

        try:
            thisInstance = Instance.objects.get(instanceName=self.instanceName)
        except:
            self.existed = False
        else:
            self.instanceName = thisInstance.instanceName
            self.vcpus = thisInstance.vcpus
            self.mem = thisInstance.mem
            self.dataDisk = thisInstance.dataDisk
            _startTime = thisInstance.startTime
            self.startTime = date2String(_startTime)
            self.useInterval = days2DateString(
                _startTime,
                thisInstance.useInterval
            )
            self.bandwidth = thisInstance.bandwidth
            self.nodeHost = thisInstance.nodeHost.node
            self.dogPort = []
            self.dogSn = {}

            try:
                self.mac = thisInstance.mac_set.all()
            except:
                self.mac = []

            self.ip = thisInstance.ip_set.all()
            self.owner = thisInstance.user.username

            try:
                self.businessMan = thisInstance.businessMan.name
            except:
                pass

            usbPorts = thisInstance.usbport_set.all()
            for i in usbPorts:
                self.dogPort.append(i.port)
                try:
                    self.dogSn[i.port] = i.dogsn.sn
                except:
                    self.dogSn[i.port] = '-'

            try:
                self.company = thisInstance.company.companyName
            except:
                self.company = None
            self.existed = True

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
        ip=None,
        mac=None,
        owner=None,
        businessMan=None
    ):
        """
        如果该实例存在，则更新该实例，如果该实例不存在则创建该实例
        """
        # 如果该实例不存在，则创建新实例
        if not self.existed:
            isSaved = self.__create(
                vmName=self.instanceName,
                vcpus=vcpus,
                mem=mem,
                dataDisk=dataDisk,
                nodeHost=nodeHost,
                owner=owner,
                startTime=startTime,
                useInterval=useInterval,
                bandwidth=bandwidth,
                company=company,
                dogSn=dogSn,
                ip=ip,
                mac=mac,
                businessMan=businessMan
            )
        else:
            isSaved = self.__update(
                vmName=vmName,
                vcpus=vcpus,
                mem=mem,
                dataDisk=dataDisk,
                nodeHost=nodeHost,
                owner=owner,
                startTime=startTime,
                useInterval=useInterval,
                bandwidth=bandwidth,
                company=company,
                dogSn=dogSn,
                ip=ip,
                mac=mac,
                businessMan=businessMan
            )

        return isSaved

    def __update(
        self,
        vmName=None,
        vcpus=None,
        mem=None,
        dataDisk=None,
        nodeHost=None,
        owner=None,
        startTime=None,
        useInterval=None,
        bandwidth=None,
        company=None,
        dogSn=None,
        ip=None,
        mac=None,
        businessMan=None
    ):
        thisInstance = Instance.objects.get(instanceName=self.instanceName)

        if dogSn:
            # try:
            self.dogSn = dogSn[0]
            self.dogPort = dogSn[1]
            # for i in dogSn:
            testPort = UsbPort.objects.filter(port=self.dogPort)
            for p in testPort:
                if p.nodeHost == NodeHost.objects.get(node=self.nodeHost):
                    thisPort = p
            thisPort.instance = thisInstance
            try:
                thisPort.dogsn.sn = self.dogSn
            except:
                try:
                    DogSN.objects.get(sn=self.dogSn)
                    return False
                except:
                    DogSN.objects.create(
                        sn=self.dogSn,
                        port=thisPort
                    ).save()
            thisPort.save()
            thisInstance.save()

            # except:
            #     pass

        if vmName:
            thisInstance.instanceName = vmName
            self.instanceName = vmName
            thisInstance.save()
            thisInstance = Instance.objects.get(instanceName=self.instanceName)

        if mem:
            self.mem = mem
            thisInstance.mem = mem
            thisInstance.save()

        if vcpus:
            self.vcpus = vcpus
            thisInstance.vcpus = vcpus
            thisInstance.save()

        if dataDisk:
            self.dataDisk = dataDisk
            thisInstance.dataDisk = dataDisk
            thisInstance.save()

        if startTime:
            newDeltaTime = (
                string2Date(self.useInterval) - string2Date(startTime)
            ).days
            thisInstance.useInterval = newDeltaTime
            self.startTime = startTime
            thisInstance.startTime = string2Date(self.startTime) +\
                datetime.timedelta(1)
            thisInstance.save()

        if useInterval:
            self.useInterval = useInterval
            thisInstance.useInterval = date2Days(
                string2Date(self.startTime),
                string2Date(self.useInterval)
            )
            thisInstance.save()

        if bandwidth:
            self.bandwidth = bandwidth
            thisInstance.bandwidth = bandwidth
            thisInstance.save()

        if nodeHost:
            self.nodeHost = nodeHost
            thisInstance.nodeHost = NodeHost.objects.get(node=nodeHost)
            thisInstance.save()

        if company:
            try:
                thisInstance.company = Company.objects.get(
                    companyName=company
                )
            except:
                Company.objects.create(companyName=company).save()
                thisInstance.company = Company.objects.get(
                    companyName=company
                )
            self.company = company
            thisInstance.save()

        if mac:
            thisMac = Mac.objects.get(macAddress=mac)
            self.mac = self.mac.append(thisMac)
            if not thisMac.instance:
                thisMac.instance = thisInstance
                thisMac.save()
            thisInstance.save()

        if ip:
            self.ip = ip
            for i in ip:
                thisIp = Ip.objects.get(ipAddress=i)
                if not thisIp.instance:
                    thisIp.instance = thisInstance
                    thisIp.save()
            thisInstance.save()

        if businessMan:
            try:
                thisBusinessMan = BusinessMan.objects.get(name=businessMan)
                thisInstance.businessMan = thisBusinessMan
                thisInstance.save()
            except:
                thisBusinessMan = thisInstance.businessMan
                thisBusinessMan.create(name=businessMan)
                thisBusinessMan.save()

        return True

    def __create(
        self,
        vmName=None,
        vcpus=None,
        mem=None,
        dataDisk=None,
        startTime=None,     #
        useInterval=None,   #
        bandwidth=None,     #
        nodeHost=None,
        company=None,   #
        dogSn=None,     #
        dogPort=None,   #
        ip=None,    #
        businessMan=None,   #
        mac=None,   #
        owner=None
    ):
        """
        创建一个新的instance, 判断ip, mac, dogPort是否已经被使用
        params: vmName: 实例名
                vcpus: cpu个数
                mem: 内存
                dataDisk: 磁盘
                startTime: 开始时间
                useInterval: 使用期限
                bandwidth: 带宽
                nodeHost: 节点
                company: 公司名
                dogSn: 狗号
                dogPort: 狗端口
                owner: 拥有者
                mac: macAddress
                ip: ipAddress
        return: boolean
        """
        try:
            thisOwner = User.objects.get(username=owner)
            thisOwner.instance_set.create(
                instanceName=vmName,
                vcpus=vcpus,
                mem=mem,
                dataDisk=dataDisk,
                bandwidth=bandwidth,
                startTime=string2Date(startTime),
                useInterval=date2Days(
                    string2Date(startTime),
                    string2Date(useInterval)
                ),
                nodeHost=NodeHost.objects.get(node=nodeHost)
            )
            thisOwner.save()
            self.instanceName = vmName
            self.vcpus = vcpus
            self.mem = mem
            self.dataDisk = dataDisk
            self.bandwidth = bandwidth
            self.startTime = string2Date(startTime)
            self.useInterval = date2Days(string2Date(startTime), string2Date(useInterval))
            self.nodeHost = nodeHost

            isSaved = self.__update(
                company=company,
                dogSn=dogSn,
                ip=ip,
                mac=mac,
                businessMan=businessMan
            )
            if isSaved:
                self.existed = True
                return True
            else:
                return False
        except:
            return False
