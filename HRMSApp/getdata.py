#!/usr/bin/env python
#-*- coding: utf-8 -*-
from models import *
from django.contrib.auth.models import User
import datetime


def getAll(user):
    """
    user: 需要的用户对象，如果是管理员则获取数据库中所有的主机信息，如果是普通用户，则返回该用户所在公司的所有主机信息
    获取所有的公司以及每一个公司的所有实例，以及每一个实例的所有计算节点
    :return: [{'companyName': companyName,
               'instances': [{'instanceName': instanceName,
                                ...
                              'nodes': [node1, node2, ...]
                             },
                             ...
                            ]
              }
              ...
             ]
    """
    companyName = user.get_profile().company.companyName
    if user.is_superuser:
        companies = Company.objects.all()
    else:
        companies = Company.objects.filter(companyName = companyName)

    # companies = Company.objects.all()                   # 获取所有的公司对象
    allCompany = []
    if not companies:
        return 'empty'
    for company in companies:                           # 对每一个公司对象进行处理
        dataCompany = {}
        companyName = company.companyName
        dataCompany.update({'companyName': companyName})

        instances = company.instance_set.all()          # 获取每一个公司的所有实例
        dataInstances = []
        for instance in instances:                      # 对每一个实例进行处理
            date = instance.startDate
            aInstance = {
                'instanceName': instance.instanceName.encode('utf-8'),
                'core': instance.vcpus.encode('utf-8'),
                'mem': instance.mem.encode('utf-8'),
                'dataDisk': instance.dataDisk.encode('utf-8'),
                'macAddress': instance.macAddress.encode('utf-8'),
                'startDate': "%s/%s/%s" % (str(date.month), str(date.day), str(date.year)),
                'useInterval': daysToDate(date, instance.useInterval),
                'bandwidth': instance.bandwidth.encode('utf-8'),
                'remotePort' : instance.remotePort.encode('utf-8'),
                'ip': instance.ip.encode('utf-8'),
                'dogSn': instance.dogSn.encode('utf-8'),
                'dogPort': instance.dogPort.encode('utf-8')
            }

            nodes = instance.node_set.all()             # 获取每一个实例的所有计算节点
            dataNodes = []
            for node in nodes:
                dataNodes.append(node.nodeName.encode('utf-8'))
            aInstance.update({'nodeName': dataNodes})

            dataInstances.append(aInstance)
        dataCompany.update({'instances': dataInstances})

        allCompany.append(dataCompany)

    return allCompany

def daysToDate(then, days):
    """
    将现在的时间now和具体的天数days相加得到最终的日期
    :param now: datetime.date对象
    :param days: 整型天数
    :return:最终的日期string对象
    """
    overtime = then + datetime.timedelta(days)
    return "%s/%s/%s" % (overtime.month, overtime.day, overtime.year)

def dateToDays(start, end):
    """
    将日期间隔转换为天数
    :param start: 开始日期string
    :param end:  结束日期string
    :return: 整型，天数
    """
    startString = start.split('/')
    endString = end.split('/')
    startDate = datetime.date(int(startString[2]), int(startString[0]), int(startString[1]))
    endDate = datetime.date(int(endString[2]), int(endString[0]), int(endString[1]))
    dayDelta = (endDate - startDate).days
    return dayDelta

def stringToDate(dateString):
    """
    将字符串转换为datetime.date对象
    :param dateString: 需要转换的字符串
    :return: datetime.date对象
    """
    dateList = dateString.split('/')
    return datetime.date(int(dateList[2]), int(dateList[0]), int(dateList[1]))

def getAllNotUsedIp():
    """
    获取所有状态为未使用的ip
    :return:ip列表
    """
    ips = Ip.objects.filter(isUsed = False)
    return [ip.ipAddress.encode('utf-8') for ip in ips]

def setIp(originalIp, newIp):
    """
    将前端传回来的两个ip进行处理
    :param originalIp: 需要将其状态改变为未使用
    :param newIp: 将其状态改变为已使用
    :return:boolean
    """
    try:
        ipO = Ip.objects.get(ipAddress = originalIp)
        ipO.isUsed = False
        ipO.save()
        ipN = Ip.objects.get(ipAddress = newIp)
        ipN.isUsed = True
        ipN.save()
        return True
    except:
        return False

def hostElementMap(hostName, hostElement, data):
    """
    将前端传入的数据修改到对应的数据库中
    :param hostName: 对应数据库中Instance表中的instanceName
    :param hostElement: 对应数据库中的Instance表中除了instanceName, dogSn, dogPort, node, ip, company的其他字段
    :param data: 将数据库中原数据修改为data
    :return: string
    """
    host = Instance.objects.get(instanceName = hostName)
    if hostElement != "hostCompany":
        try:
            if hostElement == 'hostCore':
                host.vcpus = data
            if hostElement == 'hostMem':
                host.mem = data
            if hostElement == 'hostDisk':
                host.dataDisk = data
            if hostElement == 'hostMac':
                host.macAddress = data
            if hostElement == 'hostStart':
                host.startDate = data
            if hostElement == 'hostEnd':
                host.useInterval = data
            if hostElement == 'hostRemotePort':
                host.remotePort = data
            if hostElement == 'hostDogN':
                host.dogSn = data
            if hostElement == 'hostBandwidth':
                host.bandwidth = data
            if hostElement == 'hostStart':
                dateString = data.split('/')
                newDate = datetime.date(int(dateString[2]), int(dateString[0]), int(dateString[1]))
                host.startDate = newDate
            if hostElement == 'hostEnd':
                dateString = data.split('/')
                newDate = datetime.date(int(dateString[2]), int(dateString[0]), int(dateString[1]))
                oldDate = host.startDate
                days = (newDate - oldDate).days
                host.useInterval = days
            host.save()
            return "successful"
        except:
            return "error"
    else:
        companyName = host.company.companyName
        companyId = host.company.id
        try:
            # global companyId
            thisCompany = Company.objects.get(id = companyName)
            thisCompanyId = thisCompany.id
            companyId = thisCompanyId
            host.save()

        except:
            try:
                # global companyName
                thisCompany = Company.objects.get(companyName = companyName)
                thisCompany.companyName = data
                thisCompany.save()
                return "successful"
            except:
                return "error"

def testIp(ip):
    """
    测试ip是否在ip表中存在，如果存在将其设置为已使用，如果不存在则新建
    :param ip: 传入的需要测试的ip
    :return: 新的ip或False
    """
    try:
        thisIp = Ip.objects.get(ipAddress = ip)
        if thisIp.isUsed == True:
            return
        else:
            thisIp.isUsed = True
            thisIp.save()
            return ip
    except:
        thisIp = Ip.objects.create(ipAddress = ip, isUsed = True)
        thisIp.save()
        return ip

def addNewHost(user, hostName, **hostItems):
    """
    将传入的hostName与数据库对比，如果已经存在相同的hostName，直接返回""existed，如果没有相同的hostName则将其存入数据库
    :param user: 已经登陆的用户的user对象
    :param hostName: 对应数据库中Instance表中的instanceName
    :param hostItems: 对应数据库中除了instanceName外的其他字段
    :return: 如果存在相同的hostName则返回False，如果保存数据成功则返回True
    """

    # 如果虚拟主机存在，直接返回
    try:
        Instance.objects.get(instanceName = hostName)
        return "hostExisted"
    # 如果如你主机不村在，创建新的虚拟主机
    except:
        # 如果公司已存在，则给该公司添加虚拟主机
        try:
            if user.is_superuser: # 如果该用户是管理员
                existedCompany = Company.objects.get(companyName = hostItems['hostCompany'])
                avariableIp = testIp(hostItems['hostIp'])
                if not avariableIp:
                    return "ipError"
                hostStart = stringToDate(hostItems['hostStart'])
                existedCompany.instance_set.create(instanceName = hostName,
                                                   vcpus = hostItems['hostCore'],
                                                   mem = hostItems['hostMem'],
                                                   dataDisk = hostItems['hostDisk'],
                                                   macAddress = hostItems['hostMac'],
                                                   startDate = hostStart,
                                                   useInterval = dateToDays(hostItems['hostStart'], hostItems['hostEnd']),
                                                   bandwidth = hostItems['hostBandwidth'],
                                                   remotePort = hostItems['hostRemotePort'],
                                                   ip = avariableIp,
                                                   dogSn = hostItems['hostDogN'],
                                                   dogPort = hostItems['hostDogP'])
                existedCompany.save()

                thisHost = Instance.objects.get(instanceName = hostName)
                thisHost.node_set.create(nodeName = hostItems['hostNode'])
                thisHost.save()

                return "successful"
            else: # 如果该用户不是管理员
                existedCompany = Company.objects.get(companyName = hostItems['hostCompany'])
                avariableIp = testIp(hostItems['hostIp'])
                if not avariableIp:
                    return "ipError"
                hostStart = stringToDate(hostItems['hostStart'])
                existedCompany.instance_set.create(instanceName = hostName,
                                                   vcpus = hostItems['hostCore'],
                                                   mem = hostItems['hostMem'],
                                                   dataDisk = hostItems['hostDisk'],
                                                   macAddress = hostItems['hostMac'],
                                                   startDate = hostStart,
                                                   useInterval = dateToDays(hostItems['hostStart'], hostItems['hostEnd']),
                                                   bandwidth = hostItems['hostBandwidth'],
                                                   remotePort = hostItems['hostRemotePort'],
                                                   ip = avariableIp,
                                                   dogSn = hostItems['hostDogN'],
                                                   dogPort = hostItems['hostDogP'])
                existedCompany.save()

                thisHost = Instance.objects.get(instanceName = hostName)
                thisHost.node_set.create(nodeName = hostItems['hostNode'])
                thisHost.save()

                return "successful"                
        # 如果公司不存在，则创建公司
        except:
            if user.is_superuser: # 如果该用户是管理员
                avariableIp = testIp(hostItems['hostIp'])
                if not avariableIp:
                    return "ipError"
                newCompany = Company.objects.create(companyName=hostItems['hostCompany'])
                newCompany.save()
                hostStart = stringToDate(hostItems['hostStart'])
                newInstance = Company.objects.get(companyName = hostItems['hostCompany'])
                newHost = newInstance.instance_set.create(instanceName = hostName,
                                                   vcpus = hostItems['hostCore'],
                                                   mem = hostItems['hostMem'],
                                                   dataDisk = hostItems['hostDisk'],
                                                   macAddress = hostItems['hostMac'],
                                                   startDate = hostStart,
                                                   useInterval = dateToDays(hostItems['hostStart'], hostItems['hostEnd']),
                                                   bandwidth = hostItems['hostBandwidth'],
                                                   remotePort = hostItems['hostRemotePort'],
                                                   ip = avariableIp,
                                                   dogSn = hostItems['hostDogN'],
                                                   dogPort = hostItems['hostDogP'])
                newHost.save()

                thisHost = Instance.objects.get(instanceName = hostName)
                thisHost.node_set.create(nodeName = hostItems['hostNode'])
                thisHost.save()
                return "successful"
            else: # 如果该用户不是管理员
                avariableIp = testIp(hostItems['hostIp'])
                if not avariableIp:
                    return "ipError"
                newCompany = Company.objects.create(companyName=hostItems['hostCompany'])
                newCompany.save()
                hostStart = stringToDate(hostItems['hostStart'])
                newInstance = Company.objects.get(companyName = hostItems['hostCompany'])
                newHost = newInstance.instance_set.create(instanceName = hostName,
                                                   vcpus = hostItems['hostCore'],
                                                   mem = hostItems['hostMem'],
                                                   dataDisk = hostItems['hostDisk'],
                                                   macAddress = hostItems['hostMac'],
                                                   startDate = hostStart,
                                                   useInterval = dateToDays(hostItems['hostStart'], hostItems['hostEnd']),
                                                   bandwidth = hostItems['hostBandwidth'],
                                                   remotePort = hostItems['hostRemotePort'],
                                                   ip = avariableIp,
                                                   dogSn = hostItems['hostDogN'],
                                                   dogPort = hostItems['hostDogP'])
                newHost.save()

                thisHost = Instance.objects.get(instanceName = hostName)
                thisHost.node_set.create(nodeName = hostItems['hostNode'])
                thisHost.save()
                return "successful"                

def saveIps(*ips):
    """
    将传入的ips列表的每一项逐个存入数据库的IP表中,如果ip已存在，则不做任何操作
    :param ips: 传入的ip列表
    :return: string
    """
    try:
        for ip in ips:
            try:
                Ip.objects.get(ipAddress = ip)
                continue
            except:
                thisIp = Ip.objects.create(ipAddress = ip, isUsed = False)
                thisIp.save()
                saveLog("Add a new ip '%s'" % ip)
        return 'successful'
    except:
        return 'error'

def saveLog(*logContent):
    """
    如果elements不是nothing的话，将其按照顺序存入数据库中的log表中
    :param logContent: 传入的需要记录的内容string
    :return: none
    """
    log = ""
    logTime = datetime.datetime.now()
    if len(logContent):
        for i in logContent:
            log += "\t%s" % logContent

    else:
        log += "Someone requested, but did nothing."

    newLog = Log.objects.create(content=log, logTime = logTime)
    newLog.save()

def getLog():
    """
    获取所有的日志
    :return: 所有的日志列表
    """
    logRecords = Log.objects.all()
    logCount = len(logRecords)
    if logCount <= 20:
        logRecords = logRecords
    else:
        logRecords = logRecords[logCount - 21:logCount - 1]

    logList = []
    for log in logRecords:
        logList.append("%s/%s/%s %s:%s:%s\t%s".encode('utf-8') %
                       (log.logTime.month, log.logTime.day, log.logTime.year,
                        log.logTime.hour, log.logTime.minute, log.logTime.second,
                        log.content))
    return logList

def intervalToDate(interval):
    """
    将日期区间转换为datetime.date对象的二元元素
    :param interval: 类似'2014/12/30-2014/12/31'的日期区间string
    :return: (datetime.date, datetime.date)
    """
    start, end = [datetime.datetime(int(i.split('/')[2]), int(i.split('/')[0]), int(i.split('/')[1])) for i in interval.split('-')]
    return (start, end + datetime.timedelta(1))

def conditionLog(condition, **kwargs):
    """
    处理按条件查询的日志，得到相应条件的日志
    :param kwargs: condition = time or host, interval = '2014/12/30-2014/12/31', hostname = instanceName
    :return: list logRecords
    """
    logs = []
    if condition == 'time':
        hostName = kwargs['hostName']
        dateTimeInterval = intervalToDate(kwargs['interval'])
        start = dateTimeInterval[0]
        end = dateTimeInterval[1]
        if hostName == 'empty':
            logsFilter = Log.objects.filter(logTime__range = (start, end))
        else:
            logsFilter = Log.objects.filter(logTime__range = (start, end), content__icontains = hostName)
        if not logsFilter:
            return ['no log']
        for log in logsFilter:
            logs.append(str(log.logTime) + log.content.encode('utf-8'))

    elif condition == 'hostname':
        logsFilter = Instance.objects.all()
        for i in logsFilter:
            logs.append(i.instanceName.encode('utf-8'))

    return logs

