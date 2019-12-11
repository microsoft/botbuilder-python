# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from json import loads
import aiounittest
import requests_mock

from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    MessageFactory,
    TurnContext,
    UserState,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.core.inspection import InspectionMiddleware, InspectionState
from botbuilder.schema import Activity, ActivityTypes, ChannelAccount, Entity, Mention


class TestConversationState(aiounittest.AsyncTestCase):
    async def test_scenario_with_inspection_middlware_passthrough(self):
        inspection_state = InspectionState(MemoryStorage())
        inspection_middleware = InspectionMiddleware(inspection_state)

        adapter = TestAdapter()
        adapter.use(inspection_middleware)

        inbound_activity = MessageFactory.text("hello")

        async def aux_func(context: TurnContext):
            await context.send_activity(MessageFactory.text("hi"))

        await adapter.process_activity(inbound_activity, aux_func)

        outbound_activity = adapter.activity_buffer.pop(0)

        assert outbound_activity.text, "hi"

    async def test_should_replicate_activity_data_to_listening_emulator_following_open_and_attach(
        self,
    ):
        inbound_expectation, outbound_expectation, state_expectation = (
            False,
            False,
            False,
        )

        with requests_mock.Mocker() as mocker:
            # set up our expectations in nock - each corresponds to a trace message we expect to receive in the emulator

            def match_response(request):
                nonlocal inbound_expectation, outbound_expectation, state_expectation
                r_json = loads(request.text)
                if r_json.get("type", None) != "trace":
                    return None

                if r_json.get("value", {}).get("text", None) == "hi":
                    inbound_expectation = True
                    return inbound_expectation
                if r_json.get("value", {}).get("text", None) == "echo: hi":
                    outbound_expectation = True
                    return outbound_expectation

                x_property = (
                    r_json.get("value", {})
                    .get("user_state", {})
                    .get("x", {})
                    .get("property", None)
                )
                y_property = (
                    r_json.get("value", {})
                    .get("conversation_state", {})
                    .get("y", {})
                    .get("property", None)
                )
                state_expectation = x_property == "hello" and y_property == "world"
                return state_expectation

            mocker.post(
                "https://test.com/v3/conversations/Convo1/activities",
                additional_matcher=match_response,
                json={"id": "test"},
                status_code=200,
            )

            # create the various storage and middleware objects we will be using

            storage = MemoryStorage()
            inspection_state = InspectionState(storage)
            user_state = UserState(storage)
            conversation_state = ConversationState(storage)
            inspection_middleware = InspectionMiddleware(
                inspection_state, user_state, conversation_state
            )

            # the emulator sends an /INSPECT open command - we can use another adapter here

            open_activity = MessageFactory.text("/INSPECT open")

            async def exec_test(turn_context):
                await inspection_middleware.process_command(turn_context)

            inspection_adapter = TestAdapter(exec_test, None, True)

            await inspection_adapter.receive_activity(open_activity)

            inspection_open_result_activity = inspection_adapter.activity_buffer[0]
            attach_command = inspection_open_result_activity.value

            # the logic of teh bot including replying with a message and updating user and conversation state

            x_prop = user_state.create_property("x")
            y_prop = conversation_state.create_property("y")

            async def exec_test2(turn_context):

                await turn_context.send_activity(
                    MessageFactory.text(f"echo: { turn_context.activity.text }")
                )

                (await x_prop.get(turn_context, {"property": ""}))["property"] = "hello"
                (await y_prop.get(turn_context, {"property": ""}))["property"] = "world"

                await user_state.save_changes(turn_context)
                await conversation_state.save_changes(turn_context)

            application_adapter = TestAdapter(exec_test2, None, True)

            # IMPORTANT add the InspectionMiddleware to the adapter that is running our bot

            application_adapter.use(inspection_middleware)

            await application_adapter.receive_activity(
                MessageFactory.text(attach_command)
            )

            # the attach command response is a informational message

            await application_adapter.receive_activity(MessageFactory.text("hi"))

            # trace activities should be sent to the emulator using the connector and the conversation reference

        # verify that all our expectations have been met
        assert inbound_expectation
        assert outbound_expectation
        assert state_expectation
        assert mocker.call_count, 3

    async def test_should_replicate_activity_data_to_listening_emulator_following_open_and_attach_with_at_mention(
        self,
    ):
        inbound_expectation, outbound_expectation, state_expectation = (
            False,
            False,
            False,
        )

        with requests_mock.Mocker() as mocker:
            # set up our expectations in nock - each corresponds to a trace message we expect to receive in the emulator

            def match_response(request):
                nonlocal inbound_expectation, outbound_expectation, state_expectation
                r_json = loads(request.text)
                if r_json.get("type", None) != "trace":
                    return None

                if r_json.get("value", {}).get("text", None) == "hi":
                    inbound_expectation = True
                    return inbound_expectation
                if r_json.get("value", {}).get("text", None) == "echo: hi":
                    outbound_expectation = True
                    return outbound_expectation

                x_property = (
                    r_json.get("value", {})
                    .get("user_state", {})
                    .get("x", {})
                    .get("property", None)
                )
                y_property = (
                    r_json.get("value", {})
                    .get("conversation_state", {})
                    .get("y", {})
                    .get("property", None)
                )
                state_expectation = x_property == "hello" and y_property == "world"
                return state_expectation

            mocker.post(
                "https://test.com/v3/conversations/Convo1/activities",
                additional_matcher=match_response,
                json={"id": "test"},
                status_code=200,
            )

            # create the various storage and middleware objects we will be using

            storage = MemoryStorage()
            inspection_state = InspectionState(storage)
            user_state = UserState(storage)
            conversation_state = ConversationState(storage)
            inspection_middleware = InspectionMiddleware(
                inspection_state, user_state, conversation_state
            )

            # the emulator sends an /INSPECT open command - we can use another adapter here

            open_activity = MessageFactory.text("/INSPECT open")

            async def exec_test(turn_context):
                await inspection_middleware.process_command(turn_context)

            inspection_adapter = TestAdapter(exec_test, None, True)

            await inspection_adapter.receive_activity(open_activity)

            inspection_open_result_activity = inspection_adapter.activity_buffer[0]

            recipient_id = "bot"
            attach_command = (
                f"<at>{ recipient_id }</at> { inspection_open_result_activity.value }"
            )

            # the logic of teh bot including replying with a message and updating user and conversation state

            x_prop = user_state.create_property("x")
            y_prop = conversation_state.create_property("y")

            async def exec_test2(turn_context):

                await turn_context.send_activity(
                    MessageFactory.text(f"echo: {turn_context.activity.text}")
                )

                (await x_prop.get(turn_context, {"property": ""}))["property"] = "hello"
                (await y_prop.get(turn_context, {"property": ""}))["property"] = "world"

                await user_state.save_changes(turn_context)
                await conversation_state.save_changes(turn_context)

            application_adapter = TestAdapter(exec_test2, None, True)

            # IMPORTANT add the InspectionMiddleware to the adapter that is running our bot

            application_adapter.use(inspection_middleware)

            attach_activity = Activity(
                type=ActivityTypes.message,
                text=attach_command,
                recipient=ChannelAccount(id=recipient_id),
                entities=[
                    Entity().deserialize(
                        Mention(
                            type="mention",
                            text=f"<at>{recipient_id}</at>",
                            mentioned=ChannelAccount(name="Bot", id=recipient_id),
                        ).serialize()
                    )
                ],
            )
            await application_adapter.receive_activity(attach_activity)

            # the attach command response is a informational message

            await application_adapter.receive_activity(MessageFactory.text("hi"))

            # trace activities should be sent to the emulator using the connector and the conversation reference

        # verify that all our expectations have been met
        assert inbound_expectation
        assert outbound_expectation
        assert state_expectation
        assert mocker.call_count, 3
