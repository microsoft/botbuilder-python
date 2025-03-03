# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Union

class BotFrameworkSkill:
    """
    Registration for a BotFrameworkHttpProtocol based Skill endpoint.
    """

    # pylint: disable=invalid-name
    def __init__(self, id: Union[str, None] = None, app_id: Union[str, None] = None, skill_endpoint: Union[str, None] = None):
        self.id = id
        self.app_id = app_id
        self.skill_endpoint = skill_endpoint
