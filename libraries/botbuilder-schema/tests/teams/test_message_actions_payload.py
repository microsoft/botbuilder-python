# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botframework.connector.models import (
    MessageActionsPayloadFrom,
    MessageActionsPayloadBody,
    MessageActionsPayloadAttachment,
    MessageActionsPayloadMention,
    MessageActionsPayloadReaction,
)
from botbuilder.schema.teams import MessageActionsPayload


class TestingMessageActionsPayload(aiounittest.AsyncTestCase):
    # Arrange
    test_id = "01"
    reply_to_id = "test_reply_to_id"
    message_type = "test_message_type"
    created_date_time = "01/01/2000"
    last_modified_date_time = "01/01/2000"
    deleted = False
    subject = "test_subject"
    summary = "test_summary"
    importance = "high"
    locale = "test_locale"
    link_to_message = "https://teams.microsoft/com/l/message/testing-id"
    from_property = MessageActionsPayloadFrom()
    body = MessageActionsPayloadBody
    attachment_layout = "test_attachment_layout"
    attachments = [MessageActionsPayloadAttachment()]
    mentions = [MessageActionsPayloadMention()]
    reactions = [MessageActionsPayloadReaction()]

    # Act
    message = MessageActionsPayload(
        id=test_id,
        reply_to_id=reply_to_id,
        message_type=message_type,
        created_date_time=created_date_time,
        last_modified_date_time=last_modified_date_time,
        deleted=deleted,
        subject=subject,
        summary=summary,
        importance=importance,
        locale=locale,
        link_to_message=link_to_message,
        from_property=from_property,
        body=body,
        attachment_layout=attachment_layout,
        attachments=attachments,
        mentions=mentions,
        reactions=reactions,
    )

    def test_assign_id(self, message_action_payload=message, test_id=test_id):
        # Assert
        self.assertEqual(message_action_payload.id, test_id)

    def test_assign_reply_to_id(
        self, message_action_payload=message, reply_to_id=reply_to_id
    ):
        # Assert
        self.assertEqual(message_action_payload.reply_to_id, reply_to_id)

    def test_assign_message_type(
        self, message_action_payload=message, message_type=message_type
    ):
        # Assert
        self.assertEqual(message_action_payload.message_type, message_type)

    def test_assign_created_date_time(
        self, message_action_payload=message, created_date_time=created_date_time
    ):
        # Assert
        self.assertEqual(message_action_payload.created_date_time, created_date_time)

    def test_assign_last_modified_date_time(
        self,
        message_action_payload=message,
        last_modified_date_time=last_modified_date_time,
    ):
        # Assert
        self.assertEqual(
            message_action_payload.last_modified_date_time, last_modified_date_time
        )

    def test_assign_deleted(self, message_action_payload=message, deleted=deleted):
        # Assert
        self.assertEqual(message_action_payload.deleted, deleted)

    def test_assign_subject(self, message_action_payload=message, subject=subject):
        # Assert
        self.assertEqual(message_action_payload.subject, subject)

    def test_assign_summary(self, message_action_payload=message, summary=summary):
        # Assert
        self.assertEqual(message_action_payload.summary, summary)

    def test_assign_importance(
        self, message_action_payload=message, importance=importance
    ):
        # Assert
        self.assertEqual(message_action_payload.importance, importance)

    def test_assign_locale(self, message_action_payload=message, locale=locale):
        # Assert
        self.assertEqual(message_action_payload.locale, locale)

    def test_assign_link_to_message(
        self, message_action_payload=message, link_to_message=link_to_message
    ):
        # Assert
        self.assertEqual(message_action_payload.link_to_message, link_to_message)

    def test_assign_from_property(
        self, message_action_payload=message, from_property=from_property
    ):
        # Assert
        self.assertEqual(message_action_payload.from_property, from_property)

    def test_assign_body(self, message_action_payload=message, body=body):
        # Assert
        self.assertEqual(message_action_payload.body, body)

    def test_assign_attachment_layout(
        self, message_action_payload=message, attachment_layout=attachment_layout
    ):
        # Assert
        self.assertEqual(message_action_payload.attachment_layout, attachment_layout)

    def test_assign_attachments(
        self, message_action_payload=message, attachments=attachments
    ):
        # Assert
        self.assertEqual(message_action_payload.attachments, attachments)

    def test_assign_mentions(self, message_action_payload=message, mentions=mentions):
        # Assert
        self.assertEqual(message_action_payload.mentions, mentions)

    def test_assign_reactions(
        self, message_action_payload=message, reactions=reactions
    ):
        # Assert
        self.assertEqual(message_action_payload.reactions, reactions)
