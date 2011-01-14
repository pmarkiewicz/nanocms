# -*- coding: utf-8 -*-

import logging
from django.conf.urls.defaults import patterns, url
from models import SiteSection
from views import Page

RE_SLUG = '(?P<slug>[\-\w]+)/$'

def _build_url(section):
    return patterns('', url(r'%s%s' % (section.url[1:], RE_SLUG), Page(), {'section': section.name}))

#@property
def urls():
    sections = SiteSection.objects.nav().filter(rev_url=False)
    
    if sections:
        urlp = _build_url(sections[0])
        for section in sections[1:]:
            urlp += _build_url(section)
            
        return urlp
    else:
        return []
    
urlpatterns = urls()
