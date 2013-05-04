# -*- coding: utf-8 -*-

# from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to
from software_app import settings_app


urlpatterns = patterns('',

  url( r'^apps/$', 'software_app.views.apps2', name='apps_url' ),

  url( r'^login/$', 'software_app.views.login', name='login_url' ),

  url( r'^$', redirect_to, {'url': '/%s/software/apps/' % settings_app.PROJECT_APP} ),

  )
