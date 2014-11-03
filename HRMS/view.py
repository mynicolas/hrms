#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response

def renderIndex(request):
    return render_to_response('index.html')