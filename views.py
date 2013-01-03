# -*- coding: utf-8 -*-

import json, logging, pprint
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect  # , HttpResponseNotFound, 
from django.shortcuts import render_to_response
# from django.views.decorators.cache import cache_page
from software_app import models, settings_app

log = logging.getLogger(__name__)
assert sorted(dir(settings_app)[0:-5]) == [
  u'ADMIN_CONTACT',
  u'GROUP_NAME',
  u'LOGIN_URL',
  u'PERMITTED_ADMINS', 
  u'PROJECT_APP', 
  u'SPOOFED_SHIB_JSON' ]  # rest all built-ins


def apps( request ):
  page_dict = { 
    u'api_list': models.Software.objects.filter( api=True ),
    u'production_list': models.Software.objects.filter( in_production=True ),
    u'current_development_list': models.Software.objects.filter( current_development=True ),
    u'LOGIN_URL': settings_app.LOGIN_URL, 
    }
  return render_to_response( u'software_app_templates/base.html', page_dict )


def login( request ):
  log.debug( u'login() start' )
  log.debug( u'request.META is: %s' % request.META )
  log_man = models.LoginManager( 
    REQUEST_META_DICT = request.META,
    ADMIN_CONTACT = settings_app.ADMIN_CONTACT,
    SPOOFED_SHIB_JSON = settings_app.SPOOFED_SHIB_JSON,  # for local development
    PERMITTED_ADMINS = settings_app.PERMITTED_ADMINS,
    GROUP_NAME = settings_app.GROUP_NAME  # to assign permissions-group if user is created
    )
  if log_man.check_authN() == u'failure':
    return HttpResponseForbidden( log_man.forbidden_response )
  if log_man.check_authZ() == u'failure':
    return HttpResponseForbidden( log_man.forbidden_response )
  if log_man.login_user( request ) == u'failure':  # request passed in because its session-object is updated
    return HttpResponseForbidden( log_man.forbidden_response )
  else:
    return HttpResponseRedirect( u'../../admin/software_app/software/' )
