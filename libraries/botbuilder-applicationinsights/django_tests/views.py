# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from rest_framework.decorators import api_view
from botbuilder.applicationinsights.django import common
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse


@api_view(["POST"])
def home(request):
    # Basic request, no logging.  Check BOT properties added.
    return HttpResponse("Welcome home")


@api_view(["POST"])
def botlog_event(request):
    # Simulates a bot.
    telemetry = ApplicationInsightsTelemetryClient(
        None, common.create_client()
    )  # Used shared client AppInsights uses.
    telemetry.track_event("botevent", {"foo": "bar", "moo": "cow"})
    return HttpResponse("We logged a bot event")


@api_view(["POST"])
def logger(request):
    # Log with Application Insights
    request.appinsights.client.track_trace("Logger message", {"property": "value"})
    return HttpResponse("We logged a message")


@api_view(["POST"])
def thrower(request):
    raise ValueError("This is an unexpected exception")


@api_view(["POST"])
def errorer(request):
    raise Http404("This is a 404 error")


def echoer(request):
    return HttpResponse(request.appinsights.request.id)


@api_view(["POST"])
def getid(request, id):
    return HttpResponse(str(id))


@api_view(["POST"])
def returncode(request, id):
    return HttpResponse("Status code set to %s" % id, status=int(id))


@api_view(["POST"])
def templater(request, data):
    return TemplateResponse(request, "template.html", {"context": data})


class classview:
    def __call__(self, request):
        return HttpResponse("You called a class.")
