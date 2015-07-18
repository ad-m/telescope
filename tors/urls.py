# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SummaryView.as_view(), name="summary"),
    url(r'^$', views.SummaryView.as_view(), name="home"),
    url(r'^page-(?P<page>\d+)/$', views.SummaryView.as_view(), name="summary"),
    url(r'^address-(?P<address>[0-9\.]+)/$', views.AddressView.as_view(), name="summary"),
    url(r'^summary-(?P<fingerprint>[A-F0-9]+)/$', views.DetailsView.as_view(), name="details"),
    url(r'^search/$', views.SearchView.as_view(), name="search"),
    url(r'^search/page-(?P<page>\d+)/$', views.SearchView.as_view(), name="search"),

]
