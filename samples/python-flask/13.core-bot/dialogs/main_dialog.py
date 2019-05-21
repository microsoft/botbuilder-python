# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime
from botbuilder.dialogs import ComponentDialog, DialogSet, DialogTurnStatus, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, ConfirmPrompt, PromptOptions
from botbuilder.core import MessageFactory
from .booking_dialog import BookingDialog
from booking_details import BookingDetails
from helpers.luis_helper import LuisHelper
from datatypes_date_time.timex import Timex

class MainDialog(ComponentDialog):

    def __init__(self, configuration: dict, dialog_id: str = None):
        super(MainDialog, self).__init__(dialog_id or MainDialog.__name__)

        self._configuration = configuration

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(BookingDialog())
        self.add_dialog(WaterfallDialog('WFDialog', [
            self.intro_step,
            self.act_step,
            self.final_step
        ]))

        self.initial_dialog_id = 'WFDialog'
    
    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if (not self._configuration.get("LUIS_APP_ID", "") or not self._configuration.get("LUIS_API_KEY", "") or not self._configuration.get("LUIS_API_HOST_NAME", "")):
            await step_context.context.send_activity(
                MessageFactory.text("NOTE: LUIS is not configured. To enable all capabilities, add 'LUIS_APP_ID', 'LUIS_API_KEY' and 'LUIS_API_HOST_NAME' to the config.py file."))

            return await step_context.next(None)
        else:
            return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt = MessageFactory.text("What can I help you with today?")))


    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        booking_details = await LuisHelper.excecute_luis_query(self._configuration, step_context.context) if step_context.result is not None else BookingDetails()

        # In this sample we only have a single Intent we are concerned with. However, typically a scenario
        # will have multiple different Intents each corresponding to starting a different child Dialog.

        # Run the BookingDialog giving it whatever details we have from the LUIS call, it will fill out the remainder.
        return await step_context.begin_dialog(BookingDialog.__name__, booking_details)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm, the Result here will be null.
        if (step_context.result is not None):
            result = step_context.result

            # Now we have all the booking details call the booking service.

            # If the call to the booking service was successful tell the user.
            #time_property = Timex(result.travel_date)
            #travel_date_msg = time_property.to_natural_language(datetime.now())
            msg = f'I have you booked to {result.destination} from {result.origin} on {result.travel_date}'
            await step_context.context.send_activity(MessageFactory.text(msg))
        else:
            await step_context.context.send_activity(MessageFactory.text("Thank you."))
        return await step_context.end_dialog()
