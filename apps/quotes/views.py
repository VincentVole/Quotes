# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from ..log_and_reg.models import User, Quote

# Create your views here.
def quotes(request):
	if request.session.get('user_id', False):
		context = {
			'user': User.objects.get(id=request.session['user_id']),
			'quotes': Quote.objects.all(),
			'fav_quotes': User.objects.get(id=request.session['user_id']).fav_quotes.all(),
			'messages': get_messages(request)
		}
		print User.objects.get(id=request.session['user_id']).fav_quotes.all()
		return render(request, 'quotes/quotes.html', context)
	else:
		return redirect('/')

def new_quote(request):
	if request.method == "POST":
		errors = Quote.objects.validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/quotes')
		else:
			user = User.objects.get(id=request.session['user_id']) #current user
			Quote.objects.create(content=request.POST['content'], quote_by=request.POST['quote_by'], user=user)
			return redirect('/quotes')

def user(request, id):
	if request.session.get('user_id', False):
		if list(User.objects.filter(id=id)) != []:
			context = {
				'user': User.objects.get(id=id),
				'quotes': User.objects.get(id=id).quotes.all(),
				'count': User.objects.get(id=id).quotes.count()
			}
			return render(request, 'quotes/user.html', context)
		else:
			return redirect('/quotes')
	else:
		return redirect('/')

def favorite(request, id):
	if request.method == "POST":
		user = User.objects.get(id=request.session['user_id'])
		quote = Quote.objects.get(id=id)
		quote.fav_users.add(user)
		return redirect('/quotes')
	else:
		return redirect('/')

def unfavorite(request, id):
	if request.method == "POST":
		user = User.objects.get(id=request.session['user_id'])
		quote = Quote.objects.get(id=id)
		quote.fav_users.remove(user)
		return redirect('/quotes')
	else:
		return redirect('/')