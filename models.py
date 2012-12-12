# -*- coding: utf-8 -*-

# import json, logging, pprint
# import requests
from django.db import models
from django.utils.encoding import smart_unicode
# from usep_app import settings_app

# log = logging.getLogger(__name__)


### db models ###


# class PageInfo(models.Model):
#   title_page = models.CharField( blank=True, max_length=100 )
#   title_content = models.CharField( blank=True, max_length=100 )
#   content = models.TextField( blank=True, help_text='HTML allowed.' )
#   def __unicode__(self):
#     return smart_unicode( self.title_page, u'utf-8', u'replace' )
#   class Meta:
#     verbose_name_plural = u'About page fields'


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
  