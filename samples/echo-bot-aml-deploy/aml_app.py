import asyncio

import requests
from azureml.contrib.services.aml_request import AMLRequest, rawhttp
from azureml.contrib.services.aml_response import AMLResponse
from botbuilder.core import BotFrameworkAdapterSettings, BotFrameworkAdapter
from botbuilder.schema import Activity


class EchoBot:  # pylint: disable=too-few-public-methods
    """
    Basic Echo Bot
    """

    async def on_turn(self, context):
        """
        Echo User Input on Each turn
        :param context:
        """
        # Check to see if this activity is an incoming message.
        # (It could theoretically be another type of activity.)
        if context.activity.type == 'message' and context.activity.text:
            # Check to see if the user sent a simple "quit" message.
            if context.activity.text.lower() == 'quit':
                # Send a reply.
                await context.send_activity('Bye!')
                exit(0)
            else:
                # Echo the message text back to the user.
                await context.send_activity(f'I heard you say {context.activity.text}')


def init():
    global LOOP
    global ADAPTER
    global BOT

    app_id = "XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
    app_password = "XXXXXXXXXXXXXXXXXX"
    settings = BotFrameworkAdapterSettings(app_id=app_id, app_password=app_password)
    ADAPTER = BotFrameworkAdapter(settings)

    LOOP = asyncio.get_event_loop()
    BOT = EchoBot()


@rawhttp
def run(request):
    if request.method == 'POST':
        body = request.json

        activity = Activity().deserialize(body)
        auth_header = request.headers['Authorization'] if 'Authorization' in request.headers else ''

        async def aux_func(turn_context):
            LOOP.create_task(asyncio.wait([BOT.on_turn(turn_context)]))

        try:
            task = LOOP.create_task(ADAPTER.process_activity(activity, auth_header, aux_func))
            LOOP.run_until_complete(task)
            return AMLResponse("", 201)
        except Exception as message_error:
            return AMLResponse(message_error, 417)

    if request.method == 'GET':
        respBody = str.encode("GET is supported")
        return AMLResponse(respBody, 201)

    return AMLResponse("bad request", 500)


if __name__ == "__main__":
    init()
