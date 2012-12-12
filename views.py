# -*- coding: utf-8 -*-

# import json, logging, pprint
# import requests
from django.http import HttpResponse  # HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
# from django.shortcuts import render_to_response
# from django.views.decorators.cache import cache_page
# from usep_app import settings_app, models, utility_code
# from usep_app.models import AboutPage, ContactsPage, LinksPage, PublicationsPage, TextsPage  # static pages

# log = logging.getLogger(__name__)


# @cache_page( 60 * 5 )  # 5 minutes
def apps( request ):
  # page_dict = { 
  #   u'a': 1,
  #   u'b': 2 
  #   }
  return HttpResponse( u'test', content_type=u'text/javascript; charset=utf8' )
  # return render_to_response( u'usep_templates/collectionS.html', page_dict )
