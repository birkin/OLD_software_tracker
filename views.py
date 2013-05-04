# -*- coding: utf-8 -*-

import datetime, json, logging, pprint
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect  # , HttpResponseNotFound,
from django.shortcuts import render_to_response, render
from software_app import models, settings_app

log = logging.getLogger(__name__)
assert sorted(dir(settings_app)[0:-5]) == [
  u'ADMIN_CONTACT',
  u'GROUP_NAME',
  u'LOGIN_URL',
  u'PERMITTED_ADMINS',
  u'PROJECT_APP',
  u'SPOOFED_SHIB_JSON' ]  # rest all built-ins


def apps2( request ):
  """Preps data; returns main display page or json."""  # TODO: a) delete base.html; b) cache
  ## prep data
  url_scheme, url_server = request.META[u'wsgi.url_scheme'], request.META[u'SERVER_NAME']
  api_list, production_list, current_development_list = [], [], []
  for obj in models.Software.objects.filter( api=True ):
    api_list.append( obj.make_serializable_dict( url_scheme, url_server ) )
  for obj in models.Software.objects.filter( in_production=True ):
    production_list.append( obj.make_serializable_dict( url_scheme, url_server ) )
  for obj in models.Software.objects.filter( current_development=True ):
    current_development_list.append( obj.make_serializable_dict( url_scheme, url_server ) )
  data_dict = {
    u'api_list': api_list,
    u'production_list': production_list,
    u'current_development_list': current_development_list,
    }
  ## display
  format = request.GET.get( u'format', None )
  callback = request.GET.get( u'callback', None )
  if format == u'json':
    d = { u'datetime': u'%s' % datetime.datetime.now(), u'message': u'format=json called', u'remote_ip': u'%s' % request.META[u'REMOTE_ADDR'] }
    log.info( json.dumps(d, sort_keys=True) )
    output = json.dumps( data_dict, sort_keys=True, indent=2 )
    if callback:
      output = u'%s(%s)' % ( callback, output )
    return HttpResponse( output, content_type = u'application/javascript; charset=utf-8' )
  else:
    data_dict[u'LOGIN_URL'] = settings_app.LOGIN_URL
    return render( request, u'software_app_templates/base2.html', data_dict )


def login( request ):
  """Manages login; on success takes user to app-admin."""
  log.debug( u'login() start' )
  log.debug( u'request.META is: %s' % request.META )
  log_man = models.LoginManager(
    REQUEST_META_DICT = request.META,
    ADMIN_CONTACT = settings_app.ADMIN_CONTACT,
    SPOOFED_SHIB_JSON = settings_app.SPOOFED_SHIB_JSON,   # for local development
    PERMITTED_ADMINS = settings_app.PERMITTED_ADMINS,
    GROUP_NAME = settings_app.GROUP_NAME                  # to assign permissions-group if user is created
    )
  if log_man.check_authN() == u'failure':
    return HttpResponseForbidden( log_man.forbidden_response )
  if log_man.check_authZ() == u'failure':
    return HttpResponseForbidden( log_man.forbidden_response )
  if log_man.login_user( request ) == u'failure':         # request passed in because its session-object is updated
    return HttpResponseForbidden( log_man.forbidden_response )
  else:
    return HttpResponseRedirect( u'../../admin/software_app/software/' )
