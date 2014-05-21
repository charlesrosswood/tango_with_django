from django.db import models
from django.forms import ModelForm

from rango.models import SiteUser, WallPost, WallPostComment
from django.contrib.auth.models import User

class SiteUserForm(ModelForm):
	class Meta:
		model = SiteUser

class WallPostForm(ModelForm):
	class Meta:
		model = WallPost
		fields = (
			'post',
			'user'
			)

class WallPostCommentForm(ModelForm):
	class Meta:
		model = WallPostComment
		fields = (
			'comment',
			'wall_post',
			'user'
			)

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
        	'username', 
        	'email', 
        	'password'
        	)