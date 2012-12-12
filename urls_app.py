# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from software_app import settings_app


urlpatterns = patterns('',

  ( r'^apps/$',  'software_app.views.apps' ),
  
  ( r'^login/$',  'software_app.views.login' ),
    
  ( r'^$', redirect_to, {'url': '/%s/software/apps/' % settings_app.PROJECT_APP} ),
  
  )
