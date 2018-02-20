# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import *

from microsoft.botbuilder.schema import *


class BotAssert(object):

    @staticmethod
    def activity_not_none(activity: Activity):
        if activity is None:
            raise TypeError()

    @staticmethod
    def context_not_none(context):
        if context is None:
            raise TypeError()

    @staticmethod
    def conversation_reference_not_none(reference):
        if reference is None:
            raise TypeError()

    @staticmethod
    def adapter_not_null(adapter):
        if adapter is None:
            raise TypeError()

    @staticmethod
    def activity_list_not_null(activity_list: List[Activity]):
        if activity_list is None:
            raise TypeError()

    @staticmethod
    def middleware_not_null(middleware):
        if middleware is None:
            raise TypeError()

    @staticmethod
    def middleware_set_not_null(middleware: List[object]):  # object should be Middleware
        if middleware is None:
            raise TypeError()
