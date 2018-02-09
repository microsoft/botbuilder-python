# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from abc import ABCMeta, abstractmethod


class ActivityAdapter(ABCMeta):
    @abstractmethod
    def on_receive(cls, activity):
        """
        Handler that returns incoming activities to a single consumer. The `Bot` will set this
        when the adapter is passed to its constructor. Just keep in mind that should the bots
        adapter be replaced (like when running unit tests) this handler can end up being set
        back to undefined.
        :param activity:
        :return:
        """
        pass

    @abstractmethod
    def post(cls, activities):
        """
        Called by a consumer to send outgoing set of activities to a user.
        :param activities:
        :return:
        """
        pass
