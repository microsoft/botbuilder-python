# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4 as uuid
from botbuilder.core import TurnContext, Storage
from .conversation_id_factory import ConversationIdFactoryBase
from .skill_conversation_id_factory_options import SkillConversationIdFactoryOptions
from .skill_conversation_reference import SkillConversationReference
from .skill_conversation_reference import ConversationReference


class SkillConversationIdFactory(ConversationIdFactoryBase):
    def __init__(self, storage: Storage):
        if not storage:
            raise TypeError("storage can't be None")

        self._storage = storage

    async def create_skill_conversation_id(  # pylint: disable=arguments-differ
        self, options: SkillConversationIdFactoryOptions
    ) -> str:
        """
        Creates a new `SkillConversationReference`.

        :param options: Creation options to use when creating the `SkillConversationReference`.
        :type options: :class:`botbuilder.core.skills.SkillConversationIdFactoryOptions`
        :return: ID of the created `SkillConversationReference`.
        """

        if not options:
            raise TypeError("options can't be None")

        conversation_reference = TurnContext.get_conversation_reference(
            options.activity
        )

        skill_conversation_id = str(uuid())

        # Create the SkillConversationReference instance.
        skill_conversation_reference = SkillConversationReference(
            conversation_reference=conversation_reference,
            oauth_scope=options.from_bot_oauth_scope,
        )

        # Store the SkillConversationReference using the skill_conversation_id as a key.
        skill_conversation_info = {skill_conversation_id: skill_conversation_reference}

        await self._storage.write(skill_conversation_info)

        # Return the generated skill_conversation_id (that will be also used as the conversation ID to call the skill).
        return skill_conversation_id

    async def get_conversation_reference(
        self, skill_conversation_id: str
    ) -> ConversationReference:
        return await super().get_conversation_reference(skill_conversation_id)

    async def get_skill_conversation_reference(
        self, skill_conversation_id: str
    ) -> SkillConversationReference:
        """
        Retrieve a `SkillConversationReference` with the specified ID.

        :param skill_conversation_id: The ID of the `SkillConversationReference` to retrieve.
        :type skill_conversation_id: str
        :return: `SkillConversationReference` for the specified ID; None if not found.
        """

        if not skill_conversation_id:
            raise TypeError("skill_conversation_id can't be None")

        # Get the SkillConversationReference from storage for the given skill_conversation_id.
        skill_conversation_reference = await self._storage.read([skill_conversation_id])

        return skill_conversation_reference.get(skill_conversation_id)

    async def delete_conversation_reference(self, skill_conversation_id: str):
        """
        Deletes the `SkillConversationReference` with the specified ID.

        :param skill_conversation_id: The ID of the `SkillConversationReference` to be deleted.
        :type skill_conversation_id: str
        """

        # Delete the SkillConversationReference from storage.
        await self._storage.delete([skill_conversation_id])
