# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class BotFrameworkSkill:
    """
    Registration for a BotFrameworkHttpProtocol based Skill endpoint.
    """

    # pylint: disable=invalid-name
    def __init__(self, id: str = None, app_id: str = None, skill_endpoint: str = None):
        self.id = id
        self.app_id = app_id
        self.skill_endpoint = skill_endpoint
