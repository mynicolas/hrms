#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    #companyName = models.CharField(max_length = 16, null = False,
    #default = 'company name')
    companyName = models.CharField(max_length=16, null=False, unique=True)


class NodeHost(models.Model):
    node = models.CharField(max_length=17, null=False, unique=True)


class Instance(models.Model):
    instanceName = models.CharField(max_length=10, null=False, unique=True)
    vcpus = models.CharField(max_length=10, null=False)
    mem = models.CharField(max_length=10, null=False)
    dataDisk = models.CharField(max_length=10, null=False)
    #macAddress = models.CharField(max_length=17, null=False,
    #default='aa.bb.cc.dd.ee.ff')
    startTime = models.DateTimeField(default=datetime.datetime.now())
    useInterval = models.IntegerField(max_length=255, null=False, default=365)
    bandwidth = models.CharField(max_length=4, null=False)
    #remotePort = models.CharField(max_length=8)
    #ip = models.CharField(max_length=15)
    #dogSn = models.CharField(max_length=20)
    #dogPort = models.CharField(max_length=7)
    #userId = models.ForeignKey(User)
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
    sn = models.CharField(max_length=20, null=False)
    #instance = models.ForeignKey(Instance)
    port = models.ForeignKey(UsbPort)

#class Log(models.Model):
#    content = models.TextField()
#    logTime = models.DateTimeField()
#    user = models.ForeignKey(User)


def getVms(start=0, limit=10):
    vmS = []
    for i in Instance.objects.all()[start:limit]:
        vmS.append(i.instanceName)
    return vmS


class Vm:
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
        self.exit = False

        try:
            p = Instance.objects.get(instanceName=vmName)
        except Instance.DoesNotExit:
            self.instanceName = vmName
            self.exit = False
        else:
            self.instanceName = vmName
            self.vcpus = p.vcpus
            self.mem = p.mem
            self.dataDisk = p.dataDisk
            self.startTime = p.startTime
            self.useInterval = p.useInterval
            self.bandwidth = p.bandwidth
            self.nodeHost = p.nodeHost.node
            self.company = p.company.companyName
            self.dogPort = []
            self.dogSn = {}
            self.owner = None
            self.exit = True

            for i in p.usbport_set.all():
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
        if not self.exit:
            pass
            #raise 

        if not instanceName:
            self.instanceName = vmName
            p = Instance.objects.get(instanceName=vmName)
            p = instanceName = vmName
            p.save()

        p = Instance.objects.get(instanceName=self.instanceName)

        if not mem:
            p.mem = mem

        if not mem:
            p.dataDisk = dataDisk

        if not dataDisk:
            p.dataDisk = dataDisk

        if not startTime:
            p.startTime = startTime

        if not useInterval:
            p.useInterval = useInterval

        if not bandwidth:
            p.bandwidth = bandwidth

        if not nodeHost:
            p.nodeHost = NodeHost.objects.get(node=nodeHost)

        if not company:
            p.company = Company.objects.get(companName=company)
        p.save()


    def create(
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
        pass
