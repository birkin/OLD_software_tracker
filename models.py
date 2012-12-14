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

  def __init__( self, REQUEST_META_DICT, ADMIN_CONTACT, SPOOFED_SHIB_JSON, PERMITTED_ADMINS, GROUP_NAME ):
    u'''upper-case attributes passed in'''
    self.REQUEST_META_DICT = REQUEST_META_DICT
    self.ADMIN_CONTACT = ADMIN_CONTACT
    self.SPOOFED_SHIB_JSON = SPOOFED_SHIB_JSON
    self.PERMITTED_ADMINS = PERMITTED_ADMINS
    self.GROUP_NAME = GROUP_NAME  # if user needs to be created
    self.forbidden_response = u'You are not authorized to use the admin. If you believe you should be, please contact "%s".' % self.ADMIN_CONTACT
    self.login_name = None
    self.first_name = None
    self.last_name = None
    self.email = None
    self.user = None  # django user-object
    self.authN_check = u'failure'
    self.authZ_check = u'failure'
    self.login_check = u'failure'
    try:
      self.login_name = self.REQUEST_META_DICT[ u'Shibboleth-eppn' ]
      self.first_name = self.REQUEST_META_DICT[ u'Shibboleth-givenName' ]
      self.last_name = self.REQUEST_META_DICT[ u'Shibboleth-sn' ]
      self.email = self.REQUEST_META_DICT[ u'Shibboleth-mail' ].lower()
      log.debug( u'shib info used' )
    except Exception as e:
      log.debug( u'error trying real shib info: %s' % repr(e).decode(u'utf-8', u'replace') )
      try:
        json_string = self.SPOOFED_SHIB_JSON
        try:
          d = json.loads( json_string )
        except ValueError as e2:
          log.error( u'SPOOFED_SHIB_JSON likely bad; error: %s' % repr(e2).decode(u'utf-8', u'replace') )
        self.login_name = d[ u'Shibboleth-eppn' ]
        self.first_name = d[ u'Shibboleth-givenName' ]
        self.last_name = d[ u'Shibboleth-sn' ]
        self.email = d[ u'Shibboleth-mail' ].lower()
        log.debug( u'spoofed shib info used' )
      except Exception as e3:
        log.debug( u'error using spoofed shib info: %s' % repr(e3).decode(u'utf-8', u'replace') )
    log.debug( u'LoginManager init() end' )

  def check_authN( self ):
    if self.login_name != None:
      self.authN_check = u'success'
    log.debug( u'self.authN_check: %s' % self.authN_check )
    return self.authN_check

  def check_authZ( self ):
    u'''checks eppn against list'''
    if self.login_name in self.PERMITTED_ADMINS:
      self.authZ_check = u'success'
    log.debug( u'self.authZ_check: %s' % self.authZ_check )
    return self.authZ_check

  def login_user( self, request ):
    u'''
    - authN & authZ have passed
    - request passed in because its session-object is updated
    '''
    from django.contrib import auth
    ## get or make user
    try:
      self.user = auth.models.User.objects.get( username=self.login_name )
    except Exception as e:
      log.debug( u'user-object not found: %s -- will create it' % repr(e).decode(u'utf-8', u'replace') )
      self.create_user()
    ## assign group permissions if necessary
    self.check_permissions()
    ## login
    self.user.backend = u'django.contrib.auth.backends.ModelBackend'
    auth.login( request, self.user )
    self.login_check = u'success'
    log.debug( u'self.login_check: %s' % self.login_check )
    return self.login_check

  def create_user( self ):
    from django.contrib.auth.models import User
    user = User( username=self.login_name )
    user.set_unusable_password()
    user.first_name = self.first_name
    user.last_name = self.last_name
    user.email = self.email
    user.is_staff = True   # allows admin access
    user.save()
    self.user = user
    log.debug( u'user created' )

  def check_permissions( self ):
    from django.contrib.auth.models import Group
    group = Group.objects.get( name=self.GROUP_NAME )
    if not group in self.user.groups.all():
      self.user.groups.add( group )
    log.debug( u'self.user.groups.all(): %s' % self.user.groups.all() )


  # end class LoginManager()

