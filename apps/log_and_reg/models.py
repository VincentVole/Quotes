# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def registration_validator(self, postData):
		errors = {}
		#These fields are required.
		#Name and alias fields must consist of only letters.
		NAME_REGEX = re.compile(r'^[a-zA-Z]+\s[a-zA-Z]+$')
		ALIAS_REGEX = re.compile(r'^[a-zA-Z]+$')
		if len(postData['name']) < 1:
			errors["name1"] = "Name is required!"
		else:
			if len(postData['name']) < 2:
				errors["name2"] = "Name must be at least 2 characters!"
			if not NAME_REGEX.search(postData['name']):
				errors["name3"] = "Name must consist of only letters!"
		if len(postData['alias']) < 1:
			errors["alias1"] = "Alias is required!"
		else:
			if len(postData['alias']) < 2:
				errors["alias2"] = "Alias must be at least 2 characters!"
			if not ALIAS_REGEX.search(postData['alias']):
				errors["alias3"] = "Alias must consist of only letters!"

		#Email must be a valid format.
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if len(postData['email']) < 1:
			errors["email1"] = "Email is required!"
		else:
			if not EMAIL_REGEX.match(postData['email']):
				errors["email2"] = "Email must be in a valid format!"
		if len(postData['password']) < 1:
			errors["password1"] = "Password is required!"
		else:
			#Password can be no fewer than 8 char long.
			if len(postData['password']) < 8:
				errors["password2"] = "Password must be at least 8 characters long!"

		#Password and confirmation field must match.
		if postData['password'] != postData['pass_confirm']:
			errors["password3"] = "Password and confirmation field must match!"

		#Can't make a duplicate account for one email.
		if list(User.objects.filter(email=postData['email'])) != []:
			errors["email3"] = "This email already has an account registered!"

		#Date of birth field can't be empty!
		if postData['dob'] == '':
			errors['dob1'] = "Date of birth field can't be empty!"
		else:
			#Date of birth can't be in the past!
			date_format = "%Y-%m-%d"
			input_dob = datetime.strptime(postData['dob'], date_format)
			now = datetime.now()
			if input_dob > now: #if dob given is in the future
				errors["dob2"] = "Date of birth must be in the past!"

		
		return errors;

	def login_validator(self, postData):
		errors = {}
		#Handles case where login fields are empty.
		if len(postData['email']) < 1:
			errors["login"] = "Email and password combination not found in database."
		if len(postData['password']) < 1:
			errors["login"] = "Email and password combination not found in database."
		try:
			user = User.objects.get(email=postData['email'])
			if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				errors["login"] = "Email and password combination not found in database."
		except:
			errors["login"] = "Email and password combination not found in database."
		return errors;

class QuoteManager(models.Manager):
	def validator(self, postData):
		errors = {}
		#These fields are required!
		if len(postData['quote_by']) < 1:
			errors["quote_by1"] = "Quoted By field is required!"
		elif len(postData['quote_by']) < 4:
			errors["quote_by2"] = "Quoted By field must be more than 3 characters!"
		if len(postData['content']) < 1:
			errors["content1"] = "Message field is required!"
		elif len(postData['content']) < 11:
			errors["content2"] = "Message field must be more than 10 characters!"

		return errors;


class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class Quote(models.Model):
	content = models.CharField(max_length=255)
	quote_by = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey('User', related_name="quotes") #user that posted the quote
	fav_users = models.ManyToManyField('User', related_name="fav_quotes")

	objects = QuoteManager()