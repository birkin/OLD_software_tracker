# -*- coding: utf-8 -*-

import json, logging
from django.db import models
from django.utils.encoding import smart_unicode

log = logging.getLogger(__name__)


### db models ###


class Software(models.Model):
  ACTIVITY_CHOICES = (
    ( '4', 'high' ),  # ('value-in-db', 'value-displayed')
    ( '3', 'medium' ),
    ( '2', 'low' ),
    ( '1', 'archived' ),
    )
  AUDIENCE_CHOICES = (
    ( 'public', 'public' ),
    ( 'staff', 'staff' ),    
    )
  name = models.CharField( max_length=100 )
  slug = models.SlugField()
  description = models.TextField( blank=True, help_text='HTML allowed.' )
  description_is_markdown = models.BooleanField( default=False )
  composed_of = models.ManyToManyField( 'self', null=True, blank=True, related_name='components', symmetrical=False )
  url_interactive = models.URLField( blank=True )
  url_source = models.URLField( blank=True )
  url_documentation = models.URLField( blank=True )
  url_license = models.URLField( blank=True )
  license_name = models.CharField( max_length=100, blank=True )
  contact_domain_name = models.CharField( max_length=100, blank=True )
  contact_domain_email = models.EmailField( blank=True )
  contact_technical_name = models.CharField( max_length=100, blank=True )
  contact_technical_email = models.EmailField( blank=True )
  url_feedback = models.URLField( blank=True )
  urls_pub_relations = models.TextField( blank=True, help_text='format: { "label": "url" }' )
  urls_presentations = models.TextField( blank=True, help_text='format: { "label": "url" }' )
  api = models.BooleanField( default=False )
  activity = models.CharField( max_length=20, blank=True, choices=ACTIVITY_CHOICES )
  audience = models.CharField( max_length=20, blank=True, choices=AUDIENCE_CHOICES )
  def __unicode__(self):
    return smart_unicode( self.name, u'utf-8', u'replace' )
  class Meta:
    verbose_name_plural = u'Software'


### non db models ###


class LoginManager( object ):

  def __init__( self, REQUEST_META_INFO, ADMIN_CONTACT, SPOOFED_SHIB_INFO, PERMITTED_ADMINS ):
    u'''upper-case attributes passed in'''
    self.REQUEST_META_INFO = REQUEST_META_INFO
    self.ADMIN_CONTACT = ADMIN_CONTACT
    self.SPOOFED_SHIB_INFO = SPOOFED_SHIB_INFO
    self.PERMITTED_ADMINS = PERMITTED_ADMINS
    self.forbidden_response = u'You are not authorized to use the admin. If you believe you should be, please contact "%s".' % self.ADMIN_CONTACT
    self.login_name = None  # eppn
    self.authN_check = u'failure'
    self.authZ_check = u'failure'
    self.login_check = u'failure'

  def check_authN( self ):
    u'''gets a real or (for testing) spoofed eppn'''
    log.debug( u'authN starting' )
    if u'Shibboleth-eppn' in self.REQUEST_META_INFO:
      log.debug( u'real shib-eppn found' )
      self.login_name = self.REQUEST_META_INFO[ u'Shibboleth-eppn' ]
    else:
      try:
        json_string = self.SPOOFED_SHIB_INFO
        d = json.loads( json_string )
        self.login_name = d[ u'Shibboleth-eppn' ]
        log.debug( u'spoofed shib-eppn used' )
      except Exception as e:
        log.debug( u'error handling SPOOFED_SHIB_INFO: %s' % repr(e).decode(u'utf-8', u'replace') )
    if not self.login_name == None:
      self.authN_check = u'success'
    log.debug( u'self.authN_check: %s' % self.authN_check )
    return self.authN_check

  def check_authZ( self ):
    u'''checks eppn against list'''
    log.debug( u'authZ starting' )
    if self.login_name in self.PERMITTED_ADMINS:
      self.authZ_check = u'success'
    log.debug( u'self.authZ_check: %s' % self.authZ_check )
    return self.authZ_check

  def login_user( self, request ):
    from django.contrib import auth
    u'''
    logs in user; request passed in because its session-object is updated
    TODO: auto-create user & assign to software_app group
    '''
    log.debug( u'login starting' )
    try:
      user = auth.models.User.objects.get( username=self.login_name )
      user.backend = u'django.contrib.auth.backends.ModelBackend'
      auth.login( request, user )
      self.login_check = u'success'
    except Exception as e:  # TODO auto-add user
      log.debug( u'error getting user-object: %s' % repr(e).decode(u'utf-8', u'replace') )
    log.debug( u'self.login_check: %s' % self.login_check )
    return self.login_check
