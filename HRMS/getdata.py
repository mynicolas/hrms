#-*- coding: utf-8 -*-
# from django.contrib import auth
from django.contrib.auth.models import User

def getAllUsers():
    """
    获取全部users
    :return: [{username: '', password: '', email: '', date_joined: '', last_login: '', is_active: '', is_staff: '', is_superuser: '',
               weixin: '', phone: '', question:'', answer: ''}, ... ...]
    """
    try:
        users = User.objects.all()
        allUsers = []
        for user in users:
            aUser = {}
            aUser['username'] = user.username
            aUser['password'] = user.password
            aUser['email'] = user.email
            dateJoined = user.date_joined
            aUser['date_joined'] = u"%s/%s/%s-%s:%s:%s" % \
            (dateJoined.month, dateJoined.day, dateJoined.year, 
            dateJoined.hour, dateJoined.minute, dateJoined.second)
            lastLogin = user.last_login
            aUser['last_login'] = u"%s/%s/%s-%s:%s:%s" % \
            (lastLogin.month, lastLogin.day, lastLogin.year, 
            lastLogin.hour, lastLogin.minute, lastLogin.second)
            aUser['is_active'] = str(user.is_active)
            aUser['is_staff'] = str(user.is_staff)
            aUserProfile = user.get_profile()
            aUser['companyname'] = aUserProfile.company.companyName
            aUser['weixin'] = aUserProfile.weixin
            aUser['phone'] = aUserProfile.phone
            aUser['question'] = aUserProfile.question
            aUser['answer'] = aUserProfile.answer
            allUsers.append(aUser)
        return allUsers
    except:
        return "no user"

def setPassword(username, *password):
    """
    设置用户的密码
    username: 需要被设置密码的用户名
    password: 需要设置的密码，可以为空，如果为空，则将密码设置成默认
    :return: boolean
    """
    from django.contrib.auth.hashers import make_password
    from hashlib import md5
    if password:
        md5Password = md5(password).hexdigest()
        newPassword = make_password(md5Password, None, 'pbkdf2_sha256')
    else:
        md5Password = md5('user123').hexdigest()
        newPassword = make_password(md5Password, None, 'pbkdf2_sha256')
    try:
        thisUser = User.objects.get(username = username)
        thisUser.password = newPassword
        thisUser.save()
        return True
    except:
        return False

def modifyUserStatus(*arg):
    """
    修改用户的状态，包括is_active, is_staff
    *arg: username, useritem(is_active || is_staff), value(True || False>) 
    :return: boolean
    """
    username = arg[0]
    if arg[2] == 'true':
        value = True
    elif arg[2] == 'false':
        value = False

    try:
        thisUser = User.objects.get(username = username)
        if arg[1] == 'isstaff':
            thisUser.is_staff = not value
        elif arg[1] == 'isactive':
            thisUser.is_active = not value
        thisUser.save()
        return True
    except:
        return False

