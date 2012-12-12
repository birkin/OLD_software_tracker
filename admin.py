# -*- coding: utf-8 -*-

from software_app.models import Software
from django.contrib import admin


class SoftwareAdmin(admin.ModelAdmin):
  ordering = [ 'name' ]
  list_display = [ 'name', 'audience', 'activity', 'contact_technical_email' ]
  list_filter = [ 'activity', 'api', 'audience', 'license_name' ]
  search_fields = [ 'name' ]
  # readonly_fields = [ 'code', 'settlement_code', 'region_code' ]
  

admin.site.register( Software, SoftwareAdmin )
# admin.site.register( Institution, InstitutionAdmin )
# admin.site.register( Mapper, MapperAdmin )
# admin.site.register( MapperTag )
# admin.site.register( Region, RegionAdmin )
# admin.site.register( Repository, RepositoryAdmin )
