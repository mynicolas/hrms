#-*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User

def getAllUsers():
    """
    获取全部users
    :return: [{username: '', password: '', email: '', date_joined: '', last_login: '', is_active: '', is_stuff: '', is_superuser: '',
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
            aUser['weixin'] = aUserProfile.weixin
            aUser['phone'] = aUserProfile.phone
            aUser['question'] = aUserProfile.question
            aUser['answer'] = aUserProfile.answer
            allUsers.append(aUser)
        return allUsers
    except:
        return [{'username': 'name', 'password': 'passwd', 'email': 'email', 'date_joined': 'date_joined',
                'last_login': 'last_login', 'is_active': 'is_active', 'is_stuff': 'is_stuff', 'weixin': 'weixin',
                'phone': 'phone', 'question': 'question', 'answer': 'answer'},
                {'username': 'name', 'password': 'passwd', 'email': 'email', 'date_joined': 'date_joined',
                'last_login': 'last_login', 'is_active': 'is_active', 'is_stuff': 'is_stuff', 'weixin': 'weixin',
                'phone': 'phone', 'question': 'question', 'answer': 'answer'}]
