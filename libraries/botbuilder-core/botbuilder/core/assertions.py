# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class BotAssert(object):

    @staticmethod
    def activity_not_null(activity):
        if not activity:
            raise TypeError()

    @staticmethod
    def context_not_null(context):
        if not context:
            raise TypeError()

    @staticmethod
    def conversation_reference_not_null(reference):
        if not reference:
            raise TypeError()

    @staticmethod
    def adapter_not_null(adapter):
        if not adapter:
            raise TypeError()

    @staticmethod
    def activity_list_not_null(activity_list):
        if not activity_list:
            raise TypeError()

    @staticmethod
    def middleware_not_null(middleware):
        if not middleware:
            raise TypeError()

    @staticmethod
    def middleware_set_not_null(middleware):
        if not middleware:
            raise TypeError()
