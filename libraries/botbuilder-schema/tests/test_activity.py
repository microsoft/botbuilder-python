# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.schema import (
    Activity,
    ConversationReference,
    ConversationAccount,
    ChannelAccount,
    Entity,
    ResourceResponse,
    Attachment,
)
from botbuilder.schema._connector_client_enums import ActivityTypes


class TestActivity(aiounittest.AsyncTestCase):
    def test_constructor(self):
        # Arrange
        activity = Activity()

        # Assert
        self.assertIsNotNone(activity)
        self.assertIsNone(activity.type)
        self.assertIsNone(activity.id)
        self.assertIsNone(activity.timestamp)
        self.assertIsNone(activity.local_timestamp)
        self.assertIsNone(activity.local_timezone)
        self.assertIsNone(activity.service_url)
        self.assertIsNone(activity.channel_id)
        self.assertIsNone(activity.from_property)
        self.assertIsNone(activity.conversation)
        self.assertIsNone(activity.recipient)
        self.assertIsNone(activity.text_format)
        self.assertIsNone(activity.attachment_layout)
        self.assertIsNone(activity.members_added)
        self.assertIsNone(activity.members_removed)
        self.assertIsNone(activity.reactions_added)
        self.assertIsNone(activity.reactions_removed)
        self.assertIsNone(activity.topic_name)
        self.assertIsNone(activity.history_disclosed)
        self.assertIsNone(activity.locale)
        self.assertIsNone(activity.text)
        self.assertIsNone(activity.speak)
        self.assertIsNone(activity.input_hint)
        self.assertIsNone(activity.summary)
        self.assertIsNone(activity.suggested_actions)
        self.assertIsNone(activity.attachments)
        self.assertIsNone(activity.entities)
        self.assertIsNone(activity.channel_data)
        self.assertIsNone(activity.action)
        self.assertIsNone(activity.reply_to_id)
        self.assertIsNone(activity.label)
        self.assertIsNone(activity.value_type)
        self.assertIsNone(activity.value)
        self.assertIsNone(activity.name)
        self.assertIsNone(activity.relates_to)
        self.assertIsNone(activity.code)
        self.assertIsNone(activity.expiration)
        self.assertIsNone(activity.importance)
        self.assertIsNone(activity.delivery_mode)
        self.assertIsNone(activity.listen_for)
        self.assertIsNone(activity.text_highlights)
        self.assertIsNone(activity.semantic_action)
        self.assertIsNone(activity.caller_id)

    def test_apply_conversation_reference(self):
        # Arrange
        activity = self.__create_activity()
        conversation_reference = ConversationReference(
            channel_id="123",
            service_url="serviceUrl",
            conversation=ConversationAccount(id="456"),
            user=ChannelAccount(id="abc"),
            bot=ChannelAccount(id="def"),
            activity_id="12345",
            locale="en-uS",
        )

        # Act
        activity.apply_conversation_reference(reference=conversation_reference)

        # Assert
        self.assertEqual(conversation_reference.channel_id, activity.channel_id)
        self.assertEqual(conversation_reference.locale, activity.locale)
        self.assertEqual(conversation_reference.service_url, activity.service_url)
        self.assertEqual(
            conversation_reference.conversation.id, activity.conversation.id
        )
        self.assertEqual(conversation_reference.bot.id, activity.from_property.id)
        self.assertEqual(conversation_reference.user.id, activity.recipient.id)
        self.assertEqual(conversation_reference.activity_id, activity.reply_to_id)

    def test_apply_conversation_reference_with_is_incoming_true(self):
        # Arrange
        activity = self.__create_activity()
        conversation_reference = ConversationReference(
            channel_id="cr_123",
            service_url="cr_serviceUrl",
            conversation=ConversationAccount(id="cr_456"),
            user=ChannelAccount(id="cr_abc"),
            bot=ChannelAccount(id="cr_def"),
            activity_id="cr_12345",
            locale="en-uS",
        )

        # Act
        activity.apply_conversation_reference(
            reference=conversation_reference, is_incoming=True
        )

        # Assert
        self.assertEqual(conversation_reference.channel_id, activity.channel_id)
        self.assertEqual(conversation_reference.locale, activity.locale)
        self.assertEqual(conversation_reference.service_url, activity.service_url)
        self.assertEqual(
            conversation_reference.conversation.id, activity.conversation.id
        )
        self.assertEqual(conversation_reference.user.id, activity.from_property.id)
        self.assertEqual(conversation_reference.bot.id, activity.recipient.id)
        self.assertEqual(conversation_reference.activity_id, activity.id)

    def test_as_contact_relation_update_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.contact_relation_update

        # Act
        result = activity.as_contact_relation_update_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.contact_relation_update)

    def test_as_contact_relation_update_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_contact_relation_update_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_conversation_update_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.conversation_update

        # Act
        result = activity.as_conversation_update_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.conversation_update)

    def test_as_conversation_update_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_conversation_update_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_end_of_conversation_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.end_of_conversation

        # Act
        result = activity.as_end_of_conversation_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.end_of_conversation)

    def test_as_end_of_conversation_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_end_of_conversation_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_event_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.event

        # Act
        result = activity.as_event_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.event)

    def test_as_event_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_event_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_handoff_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.handoff

        # Act
        result = activity.as_handoff_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.handoff)

    def test_as_handoff_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_handoff_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_installation_update_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.installation_update

        # Act
        result = activity.as_installation_update_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.installation_update)

    def test_as_installation_update_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_installation_update_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_invoke_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.invoke

        # Act
        result = activity.as_invoke_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.invoke)

    def test_as_invoke_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_invoke_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_message_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_message_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.message)

    def test_as_message_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.invoke

        # Act
        result = activity.as_message_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_message_activity_type_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = None

        # Act
        result = activity.as_message_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_message_delete_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message_delete

        # Act
        result = activity.as_message_delete_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.message_delete)

    def test_as_message_delete_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_message_delete_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_message_reaction_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message_reaction

        # Act
        result = activity.as_message_reaction_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.message_reaction)

    def test_as_message_reaction_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_message_reaction_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_message_update_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message_update

        # Act
        result = activity.as_message_update_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.message_update)

    def test_as_message_update_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_message_update_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_suggestion_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.suggestion

        # Act
        result = activity.as_suggestion_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.suggestion)

    def test_as_suggestion_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_suggestion_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_trace_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.trace

        # Act
        result = activity.as_trace_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.trace)

    def test_as_trace_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_trace_activity()

        # Assert
        self.assertIsNone(result)

    def test_as_typing_activity_return_activity(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.typing

        # Act
        result = activity.as_typing_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.typing)

    def test_as_typing_activity_return_none(self):
        # Arrange
        activity = self.__create_activity()
        activity.type = ActivityTypes.message

        # Act
        result = activity.as_typing_activity()

        # Assert
        self.assertIsNone(result)

    def test_create_contact_relation_update_activity(self):
        # Act
        result = Activity.create_contact_relation_update_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.contact_relation_update)

    def test_create_conversation_update_activity(self):
        # Act
        result = Activity.create_conversation_update_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.conversation_update)

    def test_create_end_of_conversation_activity(self):
        # Act
        result = Activity.create_end_of_conversation_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.end_of_conversation)

    def test_create_event_activity(self):
        # Act
        result = Activity.create_event_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.event)

    def test_create_handoff_activity(self):
        # Act
        result = Activity.create_handoff_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.handoff)

    def test_create_invoke_activity(self):
        # Act
        result = Activity.create_invoke_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.invoke)

    def test_create_message_activity(self):
        # Act
        result = Activity.create_message_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.message)

    def test_create_reply(self):
        # Arrange
        activity = self.__create_activity()
        text = "test reply"
        locale = "en-us"

        # Act
        result = activity.create_reply(text=text, locale=locale)

        # Assert
        self.assertEqual(result.text, text)
        self.assertEqual(result.locale, locale)
        self.assertEqual(result.type, ActivityTypes.message)

    def test_create_reply_without_arguments(self):
        # Arrange
        activity = self.__create_activity()

        # Act
        result = activity.create_reply()

        # Assert
        self.assertEqual(result.type, ActivityTypes.message)
        self.assertEqual(result.text, "")
        self.assertEqual(result.locale, activity.locale)

    def test_create_trace(self):
        # Arrange
        activity = self.__create_activity()
        name = "test-activity"
        value_type = "string"
        value = "test-value"
        label = "test-label"

        # Act
        result = activity.create_trace(
            name=name, value_type=value_type, value=value, label=label
        )

        # Assert
        self.assertEqual(result.type, ActivityTypes.trace)
        self.assertEqual(result.name, name)
        self.assertEqual(result.value_type, value_type)
        self.assertEqual(result.value, value)
        self.assertEqual(result.label, label)

    def test_create_trace_activity_no_recipient(self):
        # Arrange
        activity = self.__create_activity()
        activity.recipient = None

        # Act
        result = activity.create_trace("test")

        # Assert
        self.assertIsNone(result.from_property.id)
        self.assertIsNone(result.from_property.name)

    def test_crete_trace_activity_no_value_type(self):
        # Arrange
        name = "test-activity"
        value = "test-value"
        label = "test-label"

        # Act
        result = Activity.create_trace_activity(name=name, value=value, label=label)

        # Assert
        self.assertEqual(result.type, ActivityTypes.trace)
        self.assertEqual(result.value_type, type(value))
        self.assertEqual(result.label, label)

    def test_create_trace_activity(self):
        # Arrange
        name = "test-activity"
        value_type = "string"
        value = "test-value"
        label = "test-label"

        # Act
        result = Activity.create_trace_activity(
            name=name, value_type=value_type, value=value, label=label
        )

        # Assert
        self.assertEqual(result.type, ActivityTypes.trace)
        self.assertEqual(result.name, name)
        self.assertEqual(result.value_type, value_type)
        self.assertEqual(result.label, label)

    def test_create_typing_activity(self):
        # Act
        result = Activity.create_typing_activity()

        # Assert
        self.assertEqual(result.type, ActivityTypes.typing)

    def test_get_conversation_reference(self):
        # Arrange
        activity = self.__create_activity()

        # Act
        result = activity.get_conversation_reference()

        # Assert
        self.assertEqual(activity.id, result.activity_id)
        self.assertEqual(activity.from_property.id, result.user.id)
        self.assertEqual(activity.recipient.id, result.bot.id)
        self.assertEqual(activity.conversation.id, result.conversation.id)
        self.assertEqual(activity.channel_id, result.channel_id)
        self.assertEqual(activity.locale, result.locale)
        self.assertEqual(activity.service_url, result.service_url)

    def test_get_mentions(self):
        # Arrange
        mentions = [Entity(type="mention"), Entity(type="reaction")]
        activity = Activity(entities=mentions)

        # Act
        result = Activity.get_mentions(activity)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "mention")

    def test_get_reply_conversation_reference(self):
        # Arrange
        activity = self.__create_activity()
        reply = ResourceResponse(id="1234")

        # Act
        result = activity.get_reply_conversation_reference(reply=reply)

        # Assert
        self.assertEqual(reply.id, result.activity_id)
        self.assertEqual(activity.from_property.id, result.user.id)
        self.assertEqual(activity.recipient.id, result.bot.id)
        self.assertEqual(activity.conversation.id, result.conversation.id)
        self.assertEqual(activity.channel_id, result.channel_id)
        self.assertEqual(activity.locale, result.locale)
        self.assertEqual(activity.service_url, result.service_url)

    def test_has_content_empty(self):
        # Arrange
        activity_empty = Activity()

        # Act
        result_empty = activity_empty.has_content()

        # Assert
        self.assertEqual(result_empty, False)

    def test_has_content_with_text(self):
        # Arrange
        activity_with_text = Activity(text="test-text")

        # Act
        result_with_text = activity_with_text.has_content()

        # Assert
        self.assertEqual(result_with_text, True)

    def test_has_content_with_summary(self):
        # Arrange
        activity_with_summary = Activity(summary="test-summary")

        # Act
        result_with_summary = activity_with_summary.has_content()

        # Assert
        self.assertEqual(result_with_summary, True)

    def test_has_content_with_attachment(self):
        # Arrange
        activity_with_attachment = Activity(attachments=[Attachment()])

        # Act
        result_with_attachment = activity_with_attachment.has_content()

        # Assert
        self.assertEqual(result_with_attachment, True)

    def test_has_content_with_channel_data(self):
        # Arrange
        activity_with_channel_data = Activity(channel_data="test-channel-data")

        # Act
        result_with_channel_data = activity_with_channel_data.has_content()

        # Assert
        self.assertEqual(result_with_channel_data, True)

    def test_is_from_streaming_connection(self):
        # Arrange
        non_streaming = [
            "http://yayay.com",
            "https://yayay.com",
            "HTTP://yayay.com",
            "HTTPS://yayay.com",
        ]
        streaming = [
            "urn:botframework:WebSocket:wss://beep.com",
            "urn:botframework:WebSocket:http://beep.com",
            "URN:botframework:WebSocket:wss://beep.com",
            "URN:botframework:WebSocket:http://beep.com",
        ]
        activity = self.__create_activity()
        activity.service_url = None

        # Assert
        self.assertEqual(activity.is_from_streaming_connection(), False)

        for s in non_streaming:
            activity.service_url = s
            self.assertEqual(activity.is_from_streaming_connection(), False)

        for s in streaming:
            activity.service_url = s
            self.assertEqual(activity.is_from_streaming_connection(), True)

    @staticmethod
    def __create_activity() -> Activity:
        account1 = ChannelAccount(
            id="ChannelAccount_Id_1",
            name="ChannelAccount_Name_1",
            aad_object_id="ChannelAccount_aadObjectId_1",
            role="ChannelAccount_Role_1",
        )

        account2 = ChannelAccount(
            id="ChannelAccount_Id_2",
            name="ChannelAccount_Name_2",
            aad_object_id="ChannelAccount_aadObjectId_2",
            role="ChannelAccount_Role_2",
        )

        conversation_account = ConversationAccount(
            conversation_type="a",
            id="123",
            is_group=True,
            name="Name",
            role="ConversationAccount_Role",
        )

        activity = Activity(
            id="123",
            from_property=account1,
            recipient=account2,
            conversation=conversation_account,
            channel_id="ChannelId123",
            locale="en-uS",
            service_url="ServiceUrl123",
        )

        return activity
