from django.conf.urls import patterns, include, url
from rango import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^tango_with_django_project/', include('tango_with_django_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.add_csv, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^test/$', views.test, name='test'),
    url(r'^addpost/$', views.add_post, name='addpost'),
    url(r'^wall/$', views.wall, name='wall'),
    url(r'^adduser/$', views.add_user, name='adduser'),
    url(r'^signup/$', views.signup, name='signup'), 
    url(r'^addcsv/$', views.add_csv, name='addcsv'), 
    url(r'^d3stuff/$', views.d3_stuff, name='d3stuff'),
    url(r'^analysemturk/$', views.analyse_mturk, name='addcsv'), 

)
