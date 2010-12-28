# coding: utf-8

from django.contrib import admin
from models import SiteSection, Page

class CmsSiteSectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}
    list_display = ('name', 'url', 'order', 'show_in_nav')
    search_fields = ('url', 'name')

class CmsPageAdmin(admin.ModelAdmin):
    fieldsets  = (
        (None, {
                'fields': ('site_section', 'title', 'summary', 'slug', 'content')
        }),
        ('HTML Header Values', {
                'fields': ('html_title', 'meta_description', 'meta_keywords', ),'classes': 'collapse',
        }),
        ('Nav Menu Setup', {
                'fields': ('show_in_nav', 'nav_title', 'order'),'classes': 'collapse',
        }),
        ('Advanced options', {
                'classes': 'collapse', 
                'fields': ('registration_required', 'template_name',)
        }),
    )
    list_display = ('title', 'slug', 'order', 'site_section')
    list_filter = ('site_section',)
    search_fields = ('slug', 'title')
    ordering = ('slug', 'order')
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(SiteSection, CmsSiteSectionAdmin)
admin.site.register(Page, CmsPageAdmin)
