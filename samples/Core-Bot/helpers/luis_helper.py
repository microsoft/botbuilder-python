# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.ai.luis import LuisRecognizer, LuisApplication
from botbuilder.core import TurnContext

from booking_details import BookingDetails

class LuisHelper:
    
    @staticmethod
    async def excecute_luis_query(configuration: dict, turn_context: TurnContext) -> BookingDetails:
        booking_details = BookingDetails()

        try:
            luis_application = LuisApplication(
                configuration['LuisApplication'],
                configuration['LuisAPIKey'],
                'https://'+configuration['LuisAPIHostName']
            )

            recognizer = LuisRecognizer(luis_application)
            recognizer_result = await recognizer.recognize(turn_context)

            intent = sorted(recognizer_result.intents, key=recognizer_result.intents.get, reverse=True)[:1] if recognizer_result.intents else None

            if intent == 'Book_flight':
                # We need to get the result from the LUIS JSON which at every level returns an array.
                booking_details.destination = recognizer_result.entities.get("To", {}).get("Airport", [])[:1][:1]
                booking_details.origin = recognizer_result.entities.get("From", {}).get("Airport", [])[:1][:1]

                # This value will be a TIMEX. And we are only interested in a Date so grab the first result and drop the Time part.
                # TIMEX is a format that represents DateTime expressions that include some ambiguity. e.g. missing a Year.
                booking_details.travel_date = recognizer_result.entities.get("datetime", {}).get("timex", [])[:1].split('T')[0]
        except Exception as e:
            print(e)
        
        return booking_details