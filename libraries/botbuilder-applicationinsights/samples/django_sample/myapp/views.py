from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .custom_session import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient

instrumentation_key = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
telemetry = ApplicationInsightsTelemetryClient(instrumentation_key)

class MyView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        telemetry.track_event("DjangoHello")
        telemetry.flush()
        return HttpResponse("YOU POSTED DATA.")
