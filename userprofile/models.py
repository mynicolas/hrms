#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Perm(models.Model):
    user = models.ForeignKey(User, unique=True)
    query = models.TextField()
    modify = models.TextField()
    sort = models.TextField(null=True)
