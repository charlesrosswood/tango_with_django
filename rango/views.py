# Create your views here.
from django.core.management import setup_environ
from tango_with_django_project import settings
setup_environ(settings)
# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import modelformset_factory
from django.views.decorators import csrf

import datetime

from rango.models import SiteUser, WallPost, WallPostComment 
from rango.models import SiteUserForm, WallPostForm

def index(request):
	template = 'rango/index.html'
	# this gets info about the machine the request from etc....check it out
	context = RequestContext( request )

	# wall_posts = WallPost.objects.all().order_by('-date_posted')[:5]
	wall_posts = 'a post'
	wall_post_comments = []
	# for wall_post in wall_posts:
	# 	wall_post_comments.extend(WallPostComment.objects.filter(post=wall_post))

	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'wall_posts': wall_posts,
		'wall_post_comments': wall_post_comments,
	}

	return render_to_response(template, context_dict, context)
	# return HttpResponse("Rango says hello world!")

def about(request):
	template = 'rango/about.html'
	# this gets info about the machine the request from etc....check it out
	context = RequestContext( request )

	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'boldmessage':"I am important",
	}

	return render_to_response(template, context_dict, context)
	# return HttpResponse("Rango says hello world!")

def test(request):
	template = 'rango/testing_page.html'
	# this gets info about the machine the request from etc....check it out
	context = RequestContext( request )

	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'boldmessage':"I am important",
	}

	return render_to_response(template, context_dict, context)
	# return HttpResponse("Rango says hello world!")

@csrf.csrf_exempt
def add_post(request):
	form_dict = {}
	for key in request.POST:
		try:
			key = key.encode('utf-8')
			value = request.POST[key].encode('utf-8')
		except:
			key = key
			value = request.POST[key]
		form_dict.update( {key[7:]:value} )

	print 'form_dict', form_dict

	if form_dict != {}:
		post = WallPost.create(post=form_dict['post'], user=int(form_dict['user']))

	template = 'rango/addpost.html'
	# this gets info about the machine the request from etc....check it out
	context = RequestContext( request )

	posts = WallPost.objects.all().order_by('-date_posted')[:5]
	post_dicts = []
	for post in posts:
		post_dict = {}
		post_dict.update( {'user':post.user.username} )
		post_dict.update( {'post':post.post} )
		post_dict.update( {'likes':post.likes} )
		post_dict.update( {'date_posted':post.date_posted} )

		post_dicts.append( post_dict )

	# Dealing with forms to pass up
	WallPost_formset = modelformset_factory(WallPost, form=WallPostForm)
	formset = WallPost_formset()
	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'posts':post_dicts,
		'formset':formset[-1]
	}

	return render_to_response(template, context_dict, context)
	# return HttpResponse("Rango says hello world!")


@csrf.csrf_exempt
def add_user(request):
	form_dict = {}
	for key in request.POST:
		try:
			key = key.encode('utf-8')
			value = request.POST[key].encode('utf-8')
		except:
			key = key
			value = request.POST[key]
		
		form_dict.update( {key[7:]:value} )

	if form_dict != {}:
		siteuser = SiteUser.create(
			first_name=form_dict['first_name'], 
			last_name=form_dict['last_name'],
			email=form_dict['email'],
			username=form_dict['username'],
			password=form_dict['password']
			)

	template = 'rango/adduser.html'
	# this gets info about the machine the request from etc....check it out
	context = RequestContext( request )

	users = SiteUser.objects.all()[:5]
	user_dicts = []
	for user in users:
		user_dict = {}
		user_dict.update( {'first_name':user.first_name} )
		user_dict.update( {'last_name':user.last_name} )
		user_dict.update( {'username':user.username} )

		user_dicts.append( user_dict )

	# Dealing with forms to pass up
	User_formset = modelformset_factory(SiteUser, form=SiteUserForm)
	formset = User_formset()
	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'users':user_dicts,
		'formset':formset[-1]
	}

	return render_to_response(template, context_dict, context)
	# return HttpResponse("Rango says hello world!")