# Create your views here.

# from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import datetime

from rango.models import SiteUser, WallPost, WallPostComment 

def index(request):

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

	return render_to_response('rango/index.html', context_dict, context)
	# return HttpResponse("Rango says hello world!")

def about(request):

	# this gets info about the machine the request from etc....check it out
	context = RequestContext( request )

	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'boldmessage':"I am important",
	}

	return render_to_response( 'rango/about.html', context_dict, context)
	# return HttpResponse("Rango says hello world!")

def test(request):

	# this gets info about the machine the request from etc....check it out
	context = RequestContext( request )

	# the context_dict gets passed to the template and variables on the page are the keys of the dict with values of the values of the dict
	context_dict = {
		'boldmessage':"I am important",
	}

	return render_to_response( 'rango/testing_page.html', context_dict, context)
	# return HttpResponse("Rango says hello world!")