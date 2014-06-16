# Create your views here.
from django.core.management import setup_environ
from tango_with_django_project import settings
setup_environ(settings)
# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import modelformset_factory
from django.views.decorators import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import datetime
import json

from rango.models import SiteUser, WallPost, WallPostComment
from rango import analysis 
# from rango.models import SiteUserForm, WallPostForm
from rango.forms import *

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

def d3_stuff(request):
	template = 'rango/d3_stuff.html'
	# this gets info about the machine the request from etc....check it out
	context = RequestContext( request )

	context_dict = {
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

# @csrf.csrf_exempt
def wall(request):
	template = 'rango/wall.html'
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

	context_dict = {
		'posts':post_dicts,
		}

	return render_to_response(template, context_dict, context)

def add_post(request):
	template = 'rango/addpost.html'
	context = RequestContext( request )
	# form_dict = {}
	# for key in request.POST:
	# 	try:
	# 		key = key.encode('utf-8')
	# 		value = request.POST[key].encode('utf-8')
	# 	except:
	# 		key = key
	# 		value = request.POST[key]
	# 	form_dict.update( {key[7:]:value} )

	# print 'form_dict', form_dict

	if request.method == 'POST':
		post_form = WallPostForm(data=request.POST)

		if post_form.is_valid(): # method to check whether all the fields are correct
			post = post_form.save() # save the user object

			return HttpResponseRedirect(reverse('wall'))
		else:
			print post_form.errors
			
	else:
		post_form = WallPostForm()
	# if form_dict != {}:
	# 	post = WallPost.create(post=form_dict['post'], user=int(form_dict['user']))

	# this gets info about the machine the request from etc....check it out

	# posts = WallPost.objects.all().order_by('-date_posted')[:5]
	# post_dicts = []
	# for post in posts:
	# 	post_dict = {}
	# 	post_dict.update( {'user':post.user.username} )
	# 	post_dict.update( {'post':post.post} )
	# 	post_dict.update( {'likes':post.likes} )
	# 	post_dict.update( {'date_posted':post.date_posted} )

	# 	post_dicts.append( post_dict )

	# Dealing with forms to pass up
	# WallPost_formset = modelformset_factory(WallPost, form=WallPostForm)
	# formset = WallPost_formset()
	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		# 'posts':post_dicts,
		'post_form':post_form
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
	template = 'rango/adduser.html'
	context = RequestContext( request )


	if form_dict != {}:
		siteuser = SiteUser.create(
			first_name=form_dict['first_name'], 
			last_name=form_dict['last_name'],
			email=form_dict['email'],
			username=form_dict['username'],
			password=form_dict['password']
			)

	# this gets info about the machine the request from etc....check it out

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
		'formset':formset[-1],
	}

	return render_to_response(template, context_dict, context)

def signup(request):

	template = 'rango/signup.html'
	context = RequestContext( request )

	# a boolean value to note whether a user has registered or not
	registered = False

	# the easy way to populate a generated form from a POST request
	if request.method == 'POST':
		siteuser_form = UserForm(data=request.POST)

		if siteuser_form.is_valid(): # method to check whether all the fields are correct
			user = siteuser_form.save() # save the user object

			user.set_password( user.password ) # hash the password using the set_password method
			user.save() # resave the user and hashed password

			registered = True

			# return render_to_response(template, context_dict, context)
			# return HttpResponseRedirect(reverse('index'))
		else:
			print siteuser_form.errors # display any errors in the form back to the user (and in a console print)

	# else the request was blank so we need to set up a blank user form
	else:
		siteuser_form = UserForm()

	# this gets info about the machine the request from etc....check it out

	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'registered': registered,
		'siteuser_form':siteuser_form,
	}

	return render_to_response(template, context_dict, context)
	# return HttpResponse("Rango says hello world!")

def add_csv(request):

	template = 'rango/add_csv.html'
	context = RequestContext( request )

	file_uploaded = False
	graph = 'false'
	# the easy way to populate a generated form from a POST request
	if request.method == 'POST':
		csv_form = UploadFileForm(data=request.POST, files=request.FILES)

		if csv_form.is_valid(): # method to check whether all the fields are correct
			csv_file = csv_form.save() # save the user object
			file_uploaded = True
			# print 'csv_file.csv_file is', csv_file.csv_file
			analysed_txns = analysis.read_csv( csv_file )
			graph = json.dumps(analysed_txns)
			dataset_options = ['spends per day', 'frequency']
			template = 'rango/d3_new_stuff.html'
			
			context_dict = {
				'graph': graph,
				'graph_types':sorted(analysed_txns.keys(), key=str.lower),
				'dataset_options': dataset_options
			}

			return render_to_response(template, context_dict, context)
			# return HttpResponseRedirect(reverse('d3stuff'))
		else:
			print csv_form.errors # display any errors in the form back to the user (and in a console print)

	# else the request was blank so we need to set up a blank user form
	else:
		csv_form = UploadFileForm()

	# this gets info about the machine the request from etc....check it out

	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'csv_form':csv_form,
		'file_uploaded':file_uploaded,
		'graph':graph
	}

	return render_to_response(template, context_dict, context)
	# return HttpResponse("Rango says hello world!")