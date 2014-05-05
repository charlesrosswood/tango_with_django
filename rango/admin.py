from django.contrib import admin
from rango.models import SiteUser, WallPost, WallPostComment

admin.site.register(SiteUser)
admin.site.register(WallPost)
admin.site.register(WallPostComment)