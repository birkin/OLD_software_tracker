# -*- coding: utf-8 -*-

import json, pprint
from django.test import TestCase
from software_app.models import LoginManager
    

class LoginManagerTest( TestCase ):

  def test_goodShib_legit(self):
    log_man = LoginManager( 
      REQUEST_META_DICT = { u'Shibboleth-eppn': u'aa', u'Shibboleth-mail': u'bb', u'Shibboleth-sn': u'cc', u'Shibboleth-givenName': u'dd' },
      SPOOFED_SHIB_JSON = u'''{ "Shibboleth-eppn": "zz" }'''.decode(u'utf-8'),
      PERMITTED_ADMINS = [ u'aa' ],
      ADMIN_CONTACT = u'', GROUP_NAME = u'' )
    self.assertEqual( log_man.login_name, u'aa' )
    log_man.check_authN()
    self.assertEqual( log_man.authN_check, u'success' )
    log_man.check_authZ()
    self.assertEqual( log_man.authZ_check, u'success' )

  def test_noShib_legit(self):
    log_man = LoginManager( 
      REQUEST_META_DICT = {},
      SPOOFED_SHIB_JSON = u'''{ "Shibboleth-eppn": "zz", "Shibboleth-mail": "bb", "Shibboleth-sn": "cc", "Shibboleth-givenName": "dd" }'''.decode(u'utf-8'),
      PERMITTED_ADMINS = [ u'zz' ],
      ADMIN_CONTACT = u'', GROUP_NAME = u'' )
    self.assertEqual( log_man.login_name, u'zz' )
    log_man.check_authN()
    self.assertEqual( log_man.authN_check, u'success' )
    log_man.check_authZ()
    self.assertEqual( log_man.authZ_check, u'success' )
