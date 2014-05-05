import os
from datetime import datetime

from django.core.management import setup_environ
from tango_with_django_project import settings
setup_environ(settings)

from rango.models import SiteUser, WallPost, WallPostComment

users = SiteUser.objects.all()
print users
posts = WallPost.objects.all()
print posts
comments = WallPostComment.objects.all()
print comments

# date = datetime.now()
# print date, type(date)
# result_dict = SiteUser.create(first_name='Charles', last_name='Wood', email='charles.ross.wood@gmail.com', username='chazrwood', password='1')
# print result_dict
# post = "This is my second post!"
# result_dict = WallPost.create(post=post, user=users[0])
# print result_dict
# wall_post = WallPost.objects.all()[1]
# print wall_post
# # wall_post.likes += 1
# # wall_post.save()
# listy = [1,3,4]

# print listy[:5]

# comment = "This is the second comment to that post...and I've liked it"
# result_dict = WallPostComment.create(comment=comment, wall_post=wall_post, user=users[0])
# print result_dict