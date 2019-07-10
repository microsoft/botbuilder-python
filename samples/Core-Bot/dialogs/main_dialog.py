# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime
from botbuilder.dialogs import ComponentDialog, DialogSet, DialogTurnStatus, WaterfallDialog, WaterfallStepContext, \
    DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, ConfirmPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints

from .booking_dialog import BookingDialog
from cognitiveModels import FlightBooking
from booking_details import BookingDetails
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper


class MainDialog(ComponentDialog):

    def __init__(self, luis_recognizer: FlightBookingRecognizer,
                 booking_dialog: BookingDialog):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._luis_recognizer = luis_recognizer

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(booking_dialog)
        self.add_dialog(WaterfallDialog('WFDialog', [
            self.intro_step,
            self.act_step,
            self.final_step
        ]))

        self.initial_dialog_id = 'WFDialog'

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and 'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input))

            return await step_context.next(None)
        message_text = str(step_context.options) if step_context.options else "What can I help you with today?"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)

        return await step_context.prompt(TextPrompt.__name__, PromptOptions(
            prompt=prompt_message
        ))

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            return await step_context.begin_dialog(BookingDialog.__name__, BookingDetails())

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        luis_result = await self._luis_recognizer.recognize(step_context.context)
        if luis_result.top_intent().intent == FlightBooking

        # In this sample we only have a single Intent we are concerned with. However, typically a scenario
        # will have multiple different Intents each corresponding to starting a different child Dialog.

        # Run the BookingDialog giving it whatever details we have from the LUIS call, it will fill out the remainder.
        return await step_context.begin_dialog(BookingDialog.__name__, booking_details)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm, the Result here will be null.
        if step_context.result is not None:
            result = step_context.result

            # Now we have all the booking details call the booking service.

            # If the call to the booking service was successful tell the user.
            # time_property = Timex(result.travel_date)
            # travel_date_msg = time_property.to_natural_language(datetime.now())
            msg = f'I have you booked to {result.destination} from {result.origin} on {result.travel_date}'
            await step_context.context.send_activity(MessageFactory.text(msg))
        else:
            await step_context.context.send_activity(MessageFactory.text("Thank you."))
        return await step_context.end_dialog()
