# -*- coding: utf-8 -*-

import logging
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
import models

logger = logging.getLogger( __name__ )
#logger.setLevel(logging.DEBUG)

class BasePage(object):
    default_template = 'cms/default-template.html'
    login_redirect = settings.LOGIN_URL
    section = None
    
    def __init__(self, **kwargs):
        try:
            self.section = kwargs['section']
        except:
            pass

    def __call__(self, request, **kwargs):
        section = self.get_section(**kwargs)
        page = self.get_page(section, kwargs.get('slug', None))

        if page.registration_required and not request.user.is_authenticated():
            return self.auth_needed()
        
        ctx_dict = self.get_context(page, request, **kwargs)
        template = page.template_name or self.default_template
        
        return render_to_response(template, ctx_dict, context_instance=RequestContext(request))

    def get_context(self, page, request, **kwargs):
        result = kwargs.copy()
        result['page'] = page
        result['request'] = request
        
        return result
    
    def get_section(self, **kwargs):
        section_name = kwargs.get('section', None) or self.section
        if section_name:
            return get_object_or_404(models.SiteSection, name=section_name)

        return None
        
    def get_page(self, section, slug):
        raise Exception("BasePage: get_page not defined")
            
    def auth_needed(self):
        return redirect(self.login_redirect)

class Page(BasePage):
    def get_page(self, section, slug):
        if section:
            return get_object_or_404(models.Page, site_section=section, slug=slug)
        else:
            logger.warning("No section in request for slug [%s]" % slug)
            page = get_object_or_404(slug=slug)

class FirstPage(BasePage):
    def get_page(self, section, slug):
        if slug:
            logger.warning("Slug [%s] defined for FirstPage, ignored" % slug)
            
        try:
            # let's try visible pages
            return models.Page.objects.nav_first(section)
        except IndexError:
            pass    # I don't like nested try/except blocks
        
        try:
            # let's all pages
            return models.Page.objects.filter(site_section=section)[0]
        except IndexError:
            raise Http404
        