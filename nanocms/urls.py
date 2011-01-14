# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
import views

from views import *

urlpatterns = patterns('',
    url(r'(?P<slug>[\-\w]+)/$', views.Page(), name='page'),
)
