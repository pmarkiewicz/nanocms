# -*- coding: utf-8 -*-

from django.db import models
from django.core import validators
from django import forms
from django.contrib.sites.models import Site
from django.conf import settings
from tinymce.models import HTMLField

try:
    # to use south we need to declare introspection_rule
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^tinymce\.models\.HTMLField"])
except ImportError:
    pass

class SiteSectionManager(models.Manager):
    def nav(self):
        return self.get_query_set().filter(show_in_nav=True)

class SiteSection(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    url = models.CharField('url', max_length=100, unique=True, blank=False)
    rev_url = models.BooleanField('use reverse for url', default=False)
    show_in_nav = models.BooleanField('Show', default=True, db_index=True)
    order = models.PositiveIntegerField('Display Order', blank=True, null=True);
    
    class Meta:
        ordering = ('order', 'name')

    def save(self):
        # append slash if regular url
        if not self.rev_url:
            if self.url[-1] != '/':
                self.url = self.url + '/'
                
            # prepend slash
            if self.url[0] != '/':
                self.url = '/' + self.url
             
        super(SiteSection, self).save() # Call the "real" save() method.

    def __unicode__(self):
        return u"%s" % (self.name)
    
    objects = SiteSectionManager()

class PageManager(models.Manager):
    def nav(self, section):
        return self.get_query_set().filter(show_in_nav=True, site_section=section)

    def nav_first(self, section):
        return self.nav(section)[0]

class Page(models.Model):
    site_section = models.ForeignKey(SiteSection, verbose_name='Site section')
    title = models.CharField('Page Title', max_length=200)
    summary = models.CharField('Summary', max_length=100, blank=True)
    slug = models.SlugField('Slug', blank=True)
    content = HTMLField(blank=True)
    show_in_nav = models.BooleanField('Show in menu', default=False, db_index=True)
    nav_title = models.CharField(max_length=150, blank=True,
        help_text="The link text that will show in the navigation menu")
    order = models.PositiveIntegerField(blank=True, null=True,
        help_text="The order this item should appear in the menu, defaults to alphabetical if order isn't specified");
    html_title = models.CharField(max_length=250, blank=True,
        help_text="This is the browser title")
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    template_name = models.CharField('template name', max_length=70, blank=True,
        help_text="Example: 'pages/contact_page.html'. If this isn't provided, the system will use 'pages/default.html'.")
    registration_required = models.BooleanField('registration required', help_text="If this is checked, only logged-in users will be able to view the page.")

    class Meta:
        ordering = ('order', 'slug',)
        unique_together = ('site_section', 'slug', )

    objects = PageManager()

    def __unicode__(self):
        return u"%s" % (self.slug)

    #@models.permalink
    def get_absolute_url(self):
        if self.site_section.rev_url:
            return reverse(self.site_section.url, kwargs={'slug': self.slug}) 
        else:
            return '%s%s/' % (self.site_section.url, self.slug)
