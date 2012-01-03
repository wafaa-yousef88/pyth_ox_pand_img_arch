# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from django.conf.urls.defaults import *

import views

import actions
actions.autodiscover()

urlpatterns = patterns("",
    (r'^$', views.api),
)
