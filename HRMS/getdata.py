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
            aUser['date_joined'] = user.date_joined
            aUser['last_login'] = user.last_login
            aUser['is_active'] = user.is_active
            aUser['is_stuff'] = user.is_stuff
            aUser['is_superuser'] = user.is_superuser
            aUserProfile = user.get_profile()
            aUser['weixin'] = aUserProfile.weixin
            aUser['phone'] = aUserProfile.phone
            aUser['question'] = aUserProfile.question
            aUser['answer'] = aUserProfile.answer
            allUsers.append(aUser)
        return allUsers
    except:
        return
