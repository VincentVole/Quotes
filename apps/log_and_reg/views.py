# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from datetime import datetime
import bcrypt

# Create your views here.
def index(request):
	context = {
		'messages': get_messages(request)
	}
	return render(request, 'log_and_reg/index.html', context)

def add(request):
	if request.method == "POST":
		errors = User.objects.registration_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/')
		else:
			hash_pass =  bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			date_format = "%Y-%m-%d"
			input_dob = datetime.strptime(request.POST['dob'], date_format)
			user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hash_pass, dob=input_dob)
			messages.success(request, 'Welcome ' + user.alias + ', you\'ve successfully registered!', extra_tags='register')
			return redirect('/')

def login(request):
	if request.method == "POST":
		errors = User.objects.login_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/')
		else:
			user = User.objects.get(email=request.POST['email'])
			request.session['user_id'] = user.id
			return redirect('/quotes')

def logout(request):
	request.session.pop('user_id', None)
	return redirect('/')