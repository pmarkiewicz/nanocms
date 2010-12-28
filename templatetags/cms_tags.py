# coding: utf-8

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.template import Library
from django.template.loader import render_to_string
from nanocms.models import Page, SiteSection
import re
import string

register = Library()

def _cms_pages_list(path, section_name, order_by=None, limit=None):
    try:
        section = SiteSection.objects.get(name=section_name)
    except:
        return {}

    pages = Page.objects.nav(section)
    if order_by:
        pages = pages.order_by(order_by)
        
    pages = pages.only('id', 'slug', 'nav_title', 'summary')
    
    if limit:
        pages = pages[0:limit]
        
    for page in pages:
        if path == page.get_absolute_url():
            page.active = True 
            break

    return {'pages': pages}
    
@register.inclusion_tag("cms_tags/cms_menu.html") 
def cms_menu(request, section_name):
    """
    Build cms menu based on active pages that belongs to section
    
    basic template should be something like: 
            {% for page in pages %}
            <li {%if page.active%}class="active"{%endif%}><a href="{{page.get_absolute_url}}">{{page.nav_title}}</a></li>
            {% end for %}
    <ul></ul> tags should be included in base template (same rule as with forms)
    """
    
    return _cms_pages_list(request.path, section_name)

@register.inclusion_tag("cms_tags/cms_menu_news.html")
def cms_menu_news(request, section_name, max_items=5):
    """
    Build menu with recent news that belongs to section, no of item is limited to max_items.
    News are displayed from newest (decreasing order)
    
    basic template should be something like: 
            {% for page in pages %}
            <li {%if page.active%}class="active"{%endif%}>
                <a href="{{page.get_absolute_url}}">
                    {{page.nav_title}}-{{page.summary|truncatewords:5}}
                </a>
            </li>
            {% endfor %}
    <ul></ul> tags should be included in base template (same rule as with forms)
    """

    return _cms_pages_list(request.path, section_name, '-order', max_items)

@register.inclusion_tag("cms_tags/cms_news.html")
def cms_news(request, section_name):
    """
    Build page content with news that belongs to section
    News are displayed from newest (decreasing order)
    
    basic template should be something like: 
            {% for page in pages %}
            <p><a href="{{page.get_absolute_url}}">{{page.nav_title}}-{{page.summary|truncatewords:25}}</a></p>
            {% endfor %}
    """
    return _cms_pages_list(request.path, section_name, '-order')

@register.simple_tag
def cms(request, section_name, order_by=None, limit=None, template_name):
    """
    Renders set of pages that belongs to section_name using template_name
    """
    ctx_dict = _cms_pages_list(request.path, section_name, order, limit)
    return render_to_string(template_name, ctx_dict)
