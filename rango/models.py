from django.db import models

# Create your models here.

class SiteUser(models.Model):
	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=254, null=True, blank=False)
	username = models.CharField(max_length=50, null=False, blank=False)
	password = models.CharField(max_length=50, null=False, blank=False)

	def __unicode__(self):
		return str(self.first_name) + str(self.last_name)

	@classmethod
	def create(cls, first_name, last_name, email, username, password):

		success_dict = {
			'error': '',
			'result': '',
			'success': False,
		}

		identical_usernames = SiteUser.objects.filter(username__iexact=username)
		identical_first_last_names = SiteUser.objects.filter(first_name__iexact=first_name).filter(last_name__iexact=last_name)

		if identical_usernames > 0:
			success_dict['error'] += 'username already taken'
			success_dict['result'] = None
			success_dict['success'] = False

		elif identical_first_last_names > 0:
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

	# @classmethod
	# def create(cls, ):

	# 	success_dict = {
	# 		'error': '',
	# 		'result': '',
	# 		'success': False,
	# 	}



class WallPostComment(models.Model):
	comment = models.CharField(max_length=4000)
	wall_post = models.ForeignKey(WallPost)
	user = models.ForeignKey(SiteUser)
	likes = models.IntegerField(null=True, blank=True) # to count the number of likes a comment has

	def __unicode__(self):
		return "comment " + str(self.id) + " on post " + str(self.wall_post.id) + " by " + str(self.user)
