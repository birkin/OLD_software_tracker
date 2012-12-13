# -*- coding: utf-8 -*-

import json, logging, pprint
# import requests
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect  # , HttpResponseNotFound, 
# from django.shortcuts import render_to_response
# from django.views.decorators.cache import cache_page
# from usep_app import settings_app, models, utility_code
from software_app import settings_app
# from usep_app.models import AboutPage, ContactsPage, LinksPage, PublicationsPage, TextsPage  # static pages

log = logging.getLogger(__name__)
assert sorted(dir(settings_app)[0:-5]) == [
  'ADMIN_CONTACT', 
  'PERMITTED_ADMINS', 
  'PROJECT_APP', 
  'SPOOFED_SHIB_INFO' ]  # rest all built-ins


# @cache_page( 60 * 5 )  # 5 minutes
def apps( request ):
  # page_dict = { 
  #   u'a': 1,
  #   u'b': 2 
  #   }
  return HttpResponse( u'test', content_type=u'text/javascript; charset=utf8' )
  # return render_to_response( u'usep_templates/collectionS.html', page_dict )


def login( request ):
  from django.contrib import auth
  log.debug( u'login() starting' )
  log.debug( u'request.META is: %s' % request.META )
  ## authN
  forbidden_response = u'You are not authorized to use the admin. If you believe you should be, please contact "%s".' % settings_app.ADMIN_CONTACT
  login_name = u'init'
  if u'Shibboleth-eppn' in request.META:
    log.debug( u'real shib-eppn found' )
    login_name = request.META[ u'Shibboleth-eppn' ]
  else:
    try:
      json_string = settings_app.SPOOFED_SHIB_INFO
      d = json.loads( json_string )
      login_name = d[ u'Shibboleth-eppn' ]
    except Exception as e:
      log.debug( u'error handling SPOOFED_SHIB_INFO: %s' % repr(e).decode(u'utf-8', u'replace') )
  if login_name == u'init':
    log.debug( u'not a legit url access; returning forbidden' )
    return HttpResponseForbidden( forbidden_response )
  ## authZ
  if not login_name in settings_app.PERMITTED_ADMINS:
    log.debug( u'user passed authN, but not authZ; returning forbidden' )
    return HttpResponseForbidden( forbidden_response )
  else:
    log.debug( u'authN & authZ ok; trying user-object access' )
    try:
      user = auth.models.User.objects.get( username=login_name )
      user.backend = u'django.contrib.auth.backends.ModelBackend'
      auth.login( request, user )
      log.debug( u'user-object obtained & logged-in' )
      return HttpResponseRedirect( u'../../admin/software_app/software/' )
    except Exception, e:  # TODO auto-add user
      log.debug( u'error: %s' % repr(e).decode(u'utf-8', u'replace') )
      return HttpResponseForbidden( forbidden_response )
