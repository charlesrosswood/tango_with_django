from django.db import models
from django import forms

from rango.models import SiteUser, WallPost, WallPostComment
from django.contrib.auth.models import User

class SiteUserForm(forms.ModelForm):
	class Meta:
		model = SiteUser

class WallPostForm(forms.ModelForm):
	class Meta:
		model = WallPost
		fields = (
			'post',
			'user'
			)

class WallPostCommentForm(forms.ModelForm):
	class Meta:
		model = WallPostComment
		fields = (
			'comment',
			'wall_post',
			'user'
			)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
        	'username', 
        	'email', 
        	'password'
        	)