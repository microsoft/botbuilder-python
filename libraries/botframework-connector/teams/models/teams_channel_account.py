# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from .channel_account import ChannelAccount


class TeamsChannelAccount(ChannelAccount):
    """Teams channel account detailing user Azure Active Directory details.

    :param id: Channel id for the user or bot on this channel (Example:
     joe@smith.com, or @joesmith or 123456)
    :type id: str
    :param name: Display friendly name
    :type name: str
    :param given_name: Given name part of the user name.
    :type given_name: str
    :param surname: Surname part of the user name.
    :type surname: str
    :param email: Email Id of the user.
    :type email: str
    :param user_principal_name: Unique user principal name
    :type user_principal_name: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "given_name": {"key": "givenName", "type": "str"},
        "surname": {"key": "surname", "type": "str"},
        "email": {"key": "email", "type": "str"},
        "user_principal_name": {"key": "userPrincipalName", "type": "str"},
    }

    def __init__(self, **kwargs):
        super(TeamsChannelAccount, self).__init__(**kwargs)
        self.given_name = kwargs.get("given_name", None)
        self.surname = kwargs.get("surname", None)
        self.email = kwargs.get("email", None)
        self.user_principal_name = kwargs.get("user_principal_name", None)
