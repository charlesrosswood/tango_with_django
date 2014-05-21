from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

from datetime import datetime
# Create your models here.

class SiteUser(models.Model):
	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=254, null=True, blank=False)
	username = models.CharField(max_length=50, null=False, blank=False)
	password = models.CharField(max_length=50, null=False, blank=False)

	def __unicode__(self):
		return str(self.first_name) + ' ' + str(self.last_name) + ', ' + str(self.username)

	@classmethod
	def create(cls, first_name, last_name, email, username, password):

		success_dict = {
			'error': '',
			'result': '',
			'success': False,
		}

		identical_usernames = SiteUser.objects.filter(username__iexact=username)
		identical_first_last_names = SiteUser.objects.filter(first_name__iexact=first_name).filter(last_name__iexact=last_name)

		if len(identical_usernames) > 0:
			success_dict['error'] += 'username already taken'
			success_dict['result'] = None
			success_dict['success'] = False

		elif len(identical_first_last_names) > 0:
			usernames = [user.username for user in identical_first_last_names]
			success_dict['error'] += "you've already registered, your username is one of " + usernames
			success_dict['result'] = None
			success_dict['success'] = False

		else:
			user = cls(
				first_name=first_name,
				last_name=last_name,
				email=email,
				username=username,
				password=password
				)

			user.save()

			success_dict['error'] += ''
			success_dict['result'] = user
			success_dict['success'] = True

		return success_dict

class WallPost(models.Model):
	post = models.CharField(max_length=4000, null=False, blank=False)
	date_posted = models.DateTimeField('post date', null=False, blank=False)
	user = models.ForeignKey(SiteUser, null=False, blank=False)
	likes = models.IntegerField(null=True, blank=True) # to count the number of likes a post has

	def __unicode__(self):
		return "post " + str(self.id) + " posted by " + str(self.user) + " on " + str(self.date_posted)

	@classmethod
	def create(cls, post, user, date_posted=datetime.now(), likes=0):

		success_dict = {
			'error': '',
			'result': '',
			'success': False,
		}

		if isinstance(user, SiteUser) or isinstance(user, (int, float, long)):
			if isinstance(user, (int, float, long)):
				user_id = int(user)
			elif isinstance(user, SiteUser):
				user_id = user.id
			registered_user = SiteUser.objects.get(id=user_id)
			if isinstance(date_posted, datetime):
				post = cls(
					post=post,
					date_posted=date_posted,
					user=registered_user,
					likes=likes)
				post.save()

				success_dict['error'] += ''
				success_dict['result'] = post
				success_dict['success'] = True

			else:
				success_dict['error'] += 'date passed was not a datetime object'
				success_dict['result'] = None
				success_dict['success'] = False

		else:
			success_dict['error'] += 'the user passed is not registered'
			success_dict['result'] = None
			success_dict['success'] = False

		return success_dict

class WallPostComment(models.Model):
	comment = models.CharField(max_length=4000)
	wall_post = models.ForeignKey(WallPost)
	user = models.ForeignKey(SiteUser)
	likes = models.IntegerField(null=True, blank=True) # to count the number of likes a comment has
	date_posted = models.DateTimeField('post date', null=False, blank=False)

	def __unicode__(self):
		return "comment " + str(self.id) + " on post " + str(self.wall_post.id) + " by " + str(self.user)

	@classmethod
	def create(cls, comment, wall_post, user, date_posted=datetime.now(), likes=0):

		success_dict = {
			'error': '',
			'result': '',
			'success': False,
		}

		if isinstance(user, SiteUser):
			registered_users = SiteUser.objects.filter(id=user.id)
			if len(registered_users) == 1:
				if isinstance(date_posted, datetime):
					if isinstance(wall_post, WallPost):
						wallcomment = cls(
							comment=comment,
							wall_post=wall_post,
							date_posted=date_posted,
							user=user,
							likes=likes)
						wallcomment.save()

						success_dict['error'] += ''
						success_dict['result'] = wallcomment
						success_dict['success'] = True
					else:
						success_dict['error'] += 'wall post passed was not a posted wall post'
						success_dict['result'] = None
						success_dict['success'] = False						
				else:
					success_dict['error'] += 'date passed was not a datetime object'
					success_dict['result'] = None
					success_dict['success'] = False
			else:
				success_dict['error'] += 'more than one user was matched'
				success_dict['result'] = None
				success_dict['success'] = False

		else:
			success_dict['error'] += 'the user passed is not registered'
			success_dict['result'] = None
			success_dict['success'] = False

		return success_dict
