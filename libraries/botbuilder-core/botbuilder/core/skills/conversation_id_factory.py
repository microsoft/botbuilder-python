# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Union
from botbuilder.schema import ConversationReference
from .skill_conversation_id_factory_options import SkillConversationIdFactoryOptions
from .skill_conversation_reference import SkillConversationReference


class ConversationIdFactoryBase(ABC):
    """
    Handles creating conversation ids for skill and should be subclassed.

    .. remarks::
        Derive from this class to handle creation of conversation ids, retrieval of
        SkillConversationReferences and deletion.
    """

    @abstractmethod
    async def create_skill_conversation_id(
        self,
        options_or_conversation_reference: Union[
            SkillConversationIdFactoryOptions, ConversationReference
        ],
    ) -> str:
        """
        Using the options passed in, creates a conversation id and :class:`SkillConversationReference`,
         storing them for future use.

        :param options_or_conversation_reference: The options contain properties useful for generating a
         :class:`SkillConversationReference` and conversation id.
        :type options_or_conversation_reference:
         :class:`Union[SkillConversationIdFactoryOptions, ConversationReference]`

        :returns: A skill conversation id.

        .. note::
            :class:`SkillConversationIdFactoryOptions` is the preferred parameter type, while the
             :class:`SkillConversationReference` type is provided for backwards compatability.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_conversation_reference(
        self, skill_conversation_id: str
    ) -> Union[SkillConversationReference, ConversationReference]:
        """
        Retrieves a :class:`SkillConversationReference` using a conversation id passed in.

        :param skill_conversation_id: The conversation id for which to retrieve the :class:`SkillConversationReference`.
        :type skill_conversation_id: str

        .. note::
            SkillConversationReference is the preferred return type, while the :class:`SkillConversationReference`
            type is provided for backwards compatability.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_conversation_reference(self, skill_conversation_id: str):
        """
        Removes any reference to objects keyed on the conversation id passed in.
        """
        raise NotImplementedError()
