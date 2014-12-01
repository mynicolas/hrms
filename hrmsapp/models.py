#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    companyName = models.CharField(max_length=16, null=True, unique=True)


class NodeHost(models.Model):
    node = models.CharField(max_length=17, null=False, unique=True)


class Instance(models.Model):
    instanceName = models.CharField(max_length=10, null=False, unique=True)
    vcpus = models.CharField(max_length=10, null=False)
    mem = models.CharField(max_length=10, null=False)
    dataDisk = models.CharField(max_length=10, null=False)
    startTime = models.DateTimeField(default=datetime.datetime.now())
    useInterval = models.IntegerField(max_length=6, null=False, default=365)
    bandwidth = models.CharField(max_length=4, null=True)
    user = models.ForeignKey(User, null=False)
    nodeHost = models.ForeignKey(NodeHost, null=False)
    company = models.ForeignKey(Company, null=True)


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
    # startString = start.split('/')
    # endString = end.split('/')
    # startDate = datetime.date(
    #     int(startString[2]), int(startString[0]), int(startString[1])
    #     )
    # endDate = datetime.date(
    #     int(endString[2]), int(endString[0]), int(endString[1])
    #     )
    # dayDelta = (endDate - startDate).days
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
                self.mac = thisInstance.mac_set.all()[0].macAddress
            except:
                self.mac = None
            self.ip = thisInstance.ip_set.all()
            self.owner = thisInstance.user.username

            usbPorts = thisInstance.usbport_set.all()
            for i in usbPorts:
                self.dogPort.append(i.port)
                self.dogSn[i.port] = i.dogsn.sn

            try:
                self.company = thisInstance.company.companyName
            except:
                self.company = None
            self.existed = True

    def update(
        self,
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
        owner=None
    ):
        """
        如果该实例存在，则更新该实例，如果该实例不存在则创建该实例
        """
        # 如果该实例不存在，则创建新实例
        if not self.existed:
            self.__create(
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
                mac=mac
            )
        else:
            self.__update(
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
                mac=mac
            )

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
        dogPort=None,
        ip=None,
        mac=None
    ):
        thisInstance = Instance.objects.get(instanceName=self.instanceName)

        if mem:
            self.mem = mem
            thisInstance.mem = mem

        if vcpus:
            self.vcpus = vcpus
            thisInstance.vcpus = vcpus

        if dataDisk:
            self.dataDisk = dataDisk
            thisInstance.dataDisk = dataDisk

        if startTime:
            self.startTime = startTime
            thisInstance.startTime = string2Date(startTime)

        if useInterval:
            self.useInterval = useInterval
            thisInstance.useInterval = date2Days(
                string2Date(startTime),
                string2Date(useInterval)
            )

        if bandwidth:
            self.bandwidth = bandwidth
            thisInstance.bandwidth = bandwidth

        if nodeHost:
            self.nodeHost = nodeHost
            thisInstance.nodeHost = NodeHost.objects.get(node=nodeHost)

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

        if mac:
            self.mac = mac
            thisMac = Mac.objects.get(macAddress=mac)
            if not thisMac.instance:
                thisMac.instance = thisInstance
                thisMac.save()

        if dogSn:
            self.dogSn = dogSn[0]
            self.dogPort = dogSn[1]
            for i in dogSn:
                thisPort = UsbPort.objects.get(port=self.dogPort)
                thisPort.instance = thisInstance
                try:
                    thisPort.dogsn.sn = self.dogSn
                except:
                    DogSN.objects.create(sn=self.dogSn, port=thisPort).save()
                thisPort.save()

        if ip:
            self.ip = ip
            for i in ip:
                thisIp = Ip.objects.get(ipAddress=i)
                if not thisIp.instance:
                    thisIp.instance = thisInstance
                    thisIp.save()

        thisInstance.save()

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
                nodeHost=NodeHost.objects.get(node=nodeHost)
            )
            thisOwner.save()
            thisMac = Mac.objects.get(macAddress=mac)
            thisMac.instantce = Instance.objects.get(instanceName=vmName)
            thisMac.save()
            self.existed = True

            self.__update(
                vmName=vmName,
                startTime=startTime,
                useInterval=useInterval,
                company=company,
                dogSn=dogSn,
                mac=mac,
                ip=ip
            )

            return True
        except:
            return False


def getVms(start=0, end=None, user=None):
    """
    获取指定范围的实例名列表
    param: start: 范围开始索引值，end: 范围结束的索引值
    return: list(instances)
    """
    vmS = []
    if user is None:
        for i in Instance.objects.all()[start:end]:
            vmS.append(i.instanceName)
    else:
        pass
    return vmS


import pdb
pdb.run("Vm('vm4').update(vcpus='5', mem='7', dataDisk='9', bandwidth='5', nodeHost='12.34.56.78', startTime='2/1/2011', useInterval='12/2/2014', company='a', dogSn=['fdsaf', '1234'], ip=['192.168.1.4'], mac='44:44:44:44:44:44')")

# def getUserVms(user):
#     """
#     获取该当前用户的所有实例
#     param: user: 当前已登陆用户
#     return: list(dict(instances))
#     {
#     "vms": [
#             {
#                 "vmName": string,
#                  "vcpus": string,
#                  "mem": string,
#                  "dataDisk": string,
#                  "startTime": string,
#                  "useInterval": string,
#                  "bandwidth": string,
#                  "company": string,
#                  "nodeHost": string,
#                  "ip": [
#                         string,
#                         ...
#                        ],
#                  "mac": string,
#                  "usbSnPorts": [
#                                 {
#                                     "sn": string,
#                                     "port": string
#                                 },
#                                 ...
#                                ]
#              },
#              ...
#             ]
#      }
#     """
#     if not user.is_superuser:
#         return _getVms(user.instance_set.all())
#     else:
#         return _getVms(Instance.objects.all())


# def _getVms(instances):
#     """
#     获取实例
#     param: instances: Instance对象列表
#     return: list(dict(instances))
#     {
#     "vms": [
#             {
#                 "vmName": string,
#                  "vcpus": string,
#                  "mem": string,
#                  "dataDisk": string,
#                  "startTime": string,
#                  "useInterval": string,
#                  "bandwidth": string,
#                  "company": string,
#                  "nodeHost": string,
#                  "ip": [
#                         string,
#                         ...
#                        ],
#                  "mac": string,
#                  "usbSnPorts": [
#                                 {
#                                     "sn": string,
#                                     "port": string
#                                 },
#                                 ...
#                                ]
#              },
#              ...
#             ]
#      }
#     """
#     thisVms = instances
#     sendContent = {}
#     vms = []
#     for vm in thisVms:
#         aVm = {}
#         aVm["vmName"] = vm.instanceName
#         aVm["vcpus"] = vm.vcpus
#         aVm["mem"] = vm.mem
#         aVm["dataDisk"] = vm.dataDisk
#         aVm["startTime"] = _days2DateString(vm.startTime, 0)
#         aVm["useInterval"] = _days2DateString(vm.startTime, vm.useInterval)
#         aVm["bandwidth"] = vm.bandwidth
#         aVm["company"] = vm.company.companyName
#         aVm["nodeHost"] = vm.nodeHost.node
#         aVm["ip"] = _getIps(vm.ip_set.all())    # list
#         aVm["mac"] = vm.mac_set.macAddress
#         aVm["usbSnPorts"] = _getSnPorts(vm.usbport_set.all())   # list(dict)
#         vms.append(aVm)
#     sendContent["vms"] = vms
#     return sendContent


# def _getSnPorts(ports):
#     """
#     获取usbport 和 sn键值对列表
#     param: ports: usbPort对象列表
#     return: list(dict(sn, port))
#     """
#     sendContent = []
#     for aPort in ports:
#         kws = {}
#         thisPort = aPort.port
#         thisSn = aPort.dogsn_set.all()[0].sn
#         kws["sn"] = thisSn
#         kws["port"] = thisPort
#         sendContent.append(kws)
#     return sendContent


    # def addNodes(nodes):
    #     """
    #     添加node
    #     param: nodes: string(nodes)
    #     return: boolean
    #     """
    #     nodel = nodes.split(',')
    #     for aNode in nodel:
    #         try:
    #             NodeHost.objects.get(node=aNode)
    #             continue
    #         except:
    #             NodeHost.objects.create(node=aNode).save()

    #         return True


# def addIps(ips):
#     """
#     添加ip
#     param: ips: string(ips)
#     return: boolean
#     """
#     ipl = ips.split(',')
#     for ip in ipl:
#         try:
#             Ip.objects.get(ipAddress=ip)
#             continue
#         except:
#             Ip.objects.create(ipAddress=ip).save()

#     return True


# def getIps():
#     """
#     获取ip池中的所有未使用ip
#     return: dict(list(ip))
#     """
#     ips = []
#     ipos = Ip.objects.all()
#     for ip in ipos:
#         if ip.instance:
#             continue
#         else:
#             ips.append(ip.ipAddress)
#     sendContent = {"ips": ips}
#     return sendContent


# def getNodes():
#     """
#     获取node池中的所有node
#     return: dict(list(node))
#     """
#     nodes = []
#     nodeos = NodeHost.objects.all()
#     for aNode in nodeos:
#         nodes.append(aNode.node)
#     sendContent = {"nodes": nodes}
#     return sendContent


# def _getIps(ips):
#     """
#     获取ip
#     param: ips: Ip对象列表
#     return: list(ip)
#     """
#     sendContent = [ip.ipAddress for ip in ips]
#     return sendContent

# class IpMac(object):
#     def __init__(self, ipMac):
#         self.ipMac = ipMac

#         __itemType = self.ipMac.find(':')
#         if __itemType > 0:
#             self.items = Mac.objects.all()
#         else:
#             self.items = Ip.objects.all()

#     def getNotUsed(self):
#         sendContent = [i for i in self.items if not i.instance]
#         return sendContent

#     def getUsed(self):
#         sendContent = [i for i in self.items if i.instance]
#         return sendContent


# class Ip(object):
#     def __init__(self, ip):
#         self.ip = ip
#         self.isUsed = False
#         self.existed = False
#         try:
#             thisIp = Ip.objects.get(ipAddress=self.ip)
#         except Instance.DoesNotExist:
#             self.existed = False
#         else:
#             if thisIp.instance:
#                 self.isUsed = thisIp.instance[0].instanceName


# class Mac(object):
#     def __init__(self, ip):
#         self.ip = ip
#         self.isUsed = False
#         self.existed = False
#         try:
#             thisIp = Ip.objects.get(ipAddress=self.ip)
#         except Instance.DoesNotExist:
#             self.existed = False
#         else:
#             if thisIp.instance:
#                 self.isUsed = thisIp.instance[0].instanceName