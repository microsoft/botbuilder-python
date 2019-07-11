# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^logger$", views.logger, name="logger"),
    url(r"^botlog_event$", views.botlog_event, name="botlog_event"),
    url(r"^thrower$", views.thrower, name="thrower"),
    url(r"^errorer$", views.errorer, name="errorer"),
    url(r"^getid/([0-9]+)$", views.getid, name="getid"),
    url(r"^returncode/([0-9]+)$", views.returncode, name="returncode"),
    url(r"^templater/([^/]*)$", views.templater, name="templater"),
    url(r"^class$", views.classview(), name="class"),
]
