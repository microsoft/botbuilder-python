# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to use different types of rich cards.
"""


from aiohttp import web
from botbuilder.schema import (Activity, ActivityTypes,
                               AnimationCard, AudioCard, Attachment,
                               ActionTypes, CardAction,
                               CardImage, HeroCard,
                               MediaUrl, ThumbnailUrl,
                               ThumbnailCard, VideoCard,
                               ReceiptCard, SigninCard,
                               Fact, ReceiptItem)
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext,
                             ConversationState, MemoryStorage, UserState, CardFactory)
"""Import AdaptiveCard content from adjacent file"""
from adaptive_card_example import ADAPTIVE_CARD_CONTENT

APP_ID = ''
APP_PASSWORD = ''
PORT = 9000
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Create MemoryStorage, UserState and ConversationState
memory = MemoryStorage()
# Commented out user_state because it's not being used.
# user_state = UserState(memory)
conversation_state = ConversationState(memory)

# Register both State middleware on the adapter.
# Commented out user_state because it's not being used.
# ADAPTER.use(user_state)
ADAPTER.use(conversation_state)


# Methods to generate cards
def create_adaptive_card() -> Attachment:
    return CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT)


def create_animation_card() -> Attachment:
    card = AnimationCard(media=[MediaUrl(url='http://i.giphy.com/Ki55RUbOV5njy.gif')],
                         title='Microsoft Bot Framework',
                         subtitle='Animation Card')
    return CardFactory.animation_card(card)


def create_audio_card() -> Attachment:
    card = AudioCard(media=[MediaUrl(url='http://www.wavlist.com/movies/004/father.wav')],
                     title='I am your father',
                     subtitle='Star Wars: Episode V - The Empire Strikes Back',
                     text='The Empire Strikes Back (also known as Star Wars: Episode V – The Empire Strikes '
                          'Back) is a 1980 American epic space opera film directed by Irvin Kershner. Leigh '
                          'Brackett and Lawrence Kasdan wrote the screenplay, with George Lucas writing the '
                          'film\'s story and serving as executive producer. The second installment in the '
                          'original Star Wars trilogy, it was produced by Gary Kurtz for Lucasfilm Ltd. and '
                          'stars Mark Hamill, Harrison Ford, Carrie Fisher, Billy Dee Williams, Anthony '
                          'Daniels, David Prowse, Kenny Baker, Peter Mayhew and Frank Oz.',
                     image=ThumbnailUrl(url='https://upload.wikimedia.org/wikipedia/en/3/3c/SW_-_Empire_Strikes_Back.jpg'),
                     buttons=[CardAction(type=ActionTypes.open_url,
                                         title='Read more',
                                         value='https://en.wikipedia.org/wiki/The_Empire_Strikes_Back')])
    return CardFactory.audio_card(card)


def create_hero_card() -> Attachment:
    card = HeroCard(title='',
                    images=[CardImage(url='https://sec.ch9.ms/ch9/7ff5/e07cfef0-aa3b-40bb-9baa-7c9ef8ff7ff5/buildreactionbotframework_960.jpg')],
                    buttons=[CardAction(type=ActionTypes.open_url,
                                        title='Get Started',
                                        value='https://docs.microsoft.com/en-us/azure/bot-service/')],
                    )
    return CardFactory.hero_card(card)


def create_video_card() -> Attachment:
    card = VideoCard(title='Big Buck Bunny',
                     subtitle='by the Blender Institute',
                     text='Big Buck Bunny (code-named Peach) is a short computer-animated comedy film by the Blender '
                          'Institute, part of the Blender Foundation. Like the foundation\'s previous film Elephants '
                          'Dream, the film was made using Blender, a free software application for animation made by '
                          'the same foundation. It was released as an open-source film under Creative Commons License '
                          'Attribution 3.0.',
                     media=[MediaUrl(url='http://download.blender.org/peach/bigbuckbunny_movies/'
                                          'BigBuckBunny_320x180.mp4')],
                     buttons=[CardAction(type=ActionTypes.open_url,
                                         title='Learn More',
                                         value='https://peach.blender.org/')])
    return CardFactory.video_card(card)


def create_receipt_card() -> Attachment:
    card = ReceiptCard(title='John Doe', facts=[Fact(key="Order Number", value="1234"),
                                                Fact(key="Payment Method", value="VISA 5555-****")],
                       items=[ReceiptItem(title="Data Transfer", price="$38.45", quantity="368",
                                          image=CardImage(url="https://github.com/amido/azure-vector-icons/raw/master/"
                                                              "renders/traffic-manager.png")),
                              ReceiptItem(title="App Service", price="$45.00", quantity="720",
                                          image=CardImage(url="https://github.com/amido/azure-vector-icons/raw/master/"
                                                              "renders/cloud-service.png"))],
                       tax="$7.50",
                       total="90.95",
                       buttons=[CardAction(type=ActionTypes.open_url, title="More Information",
                                           value="https://azure.microsoft.com/en-us/pricing/details/bot-service/")]
                       )
    return CardFactory.receipt_card(card)


def create_signin_card() -> Attachment:
    card = SigninCard(text="BotFramework Sign-in Card", buttons=[CardAction(type=ActionTypes.signin,
                                                                            title="Sign-in",
                                                                            value="https://login.microsoftonline.com")])
    return CardFactory.signin_card(card)


def create_thumbnail_card() -> Attachment:
    card = ThumbnailCard(title="BotFramework Thumbnail Card", subtitle="Your bots — wherever your users are talking",
                         text="Build and connect intelligent bots to interact with your users naturally wherever"
                              " they are, from text/sms to Skype, Slack, Office 365 mail and other popular services.",
                         images=[CardImage(url="https://sec.ch9.ms/ch9/7ff5/"
                                               "e07cfef0-aa3b-40bb-9baa-7c9ef8ff7ff5/"
                                               "buildreactionbotframework_960.jpg")],
                         buttons=[CardAction(type=ActionTypes.open_url, title="Get Started",
                                             value="https://docs.microsoft.com/en-us/azure/bot-service/")])
    return CardFactory.thumbnail_card(card)


async def create_reply_activity(request_activity: Activity, text: str, attachment: Attachment = None) -> Activity:
    activity = Activity(
        type=ActivityTypes.message,
        channel_id=request_activity.channel_id,
        conversation=request_activity.conversation,
        recipient=request_activity.from_property,
        from_property=request_activity.recipient,
        text=text,
        service_url=request_activity.service_url)
    if attachment:
        activity.attachments = [attachment]
    return activity


async def handle_message(context: TurnContext) -> web.Response:
    # Access the state for the conversation between the user and the bot.
    state = await conversation_state.get(context)
    if hasattr(state, 'in_prompt'):
        if state.in_prompt:
            state.in_prompt = False
            return await card_response(context)
        else:
            state.in_prompt = True
            prompt_message = await create_reply_activity(context.activity, 'Which card would you like to see?\n'
                                                                           '(1) Adaptive Card\n'
                                                                           '(2) Animation Card\n'
                                                                           '(3) Audio Card\n'
                                                                           '(4) Hero Card\n'
                                                                           '(5) Receipt Card\n'
                                                                           '(6) Signin Card\n'
                                                                           '(7) Thumbnail Card\n'
                                                                           '(8) Video Card\n'
                                                                           '(9) All Cards')
            await context.send_activity(prompt_message)
            return web.Response(status=202)
    else:
        state.in_prompt = True
        prompt_message = await create_reply_activity(context.activity, 'Which card would you like to see?\n'
                                                                       '(1) Adaptive Card\n'
                                                                       '(2) Animation Card\n'
                                                                       '(3) Audio Card\n'
                                                                       '(4) Hero Card\n'
                                                                       '(5) Receipt Card\n'
                                                                       '(6) Signin Card\n'
                                                                       '(7) Thumbnail Card\n'
                                                                       '(8) Video Card\n'
                                                                       '(9) All Cards')
        await context.send_activity(prompt_message)
        return web.Response(status=202)


async def card_response(context: TurnContext) -> web.Response:
    response = context.activity.text.strip()
    choice_dict = {
        '1': [create_adaptive_card], 'adaptive card': [create_adaptive_card],
        '2': [create_animation_card], 'animation card': [create_animation_card],
        '3': [create_audio_card], 'audio card': [create_audio_card],
        '4': [create_hero_card], 'hero card': [create_hero_card],
        '5': [create_receipt_card], 'receipt card': [create_receipt_card],
        '6': [create_signin_card], 'signin card': [create_signin_card],
        '7': [create_thumbnail_card], 'thumbnail card': [create_thumbnail_card],
        '8': [create_video_card], 'video card': [create_video_card],
        '9': [create_adaptive_card, create_animation_card, create_audio_card, create_hero_card,
              create_receipt_card, create_signin_card, create_thumbnail_card, create_video_card],
        'all cards': [create_adaptive_card, create_animation_card, create_audio_card, create_hero_card,
                      create_receipt_card, create_signin_card, create_thumbnail_card, create_video_card]
    }

    # Get the functions that will generate the card(s) for our response
    # If the stripped response from the user is not found in our choice_dict, default to None
    choice = choice_dict.get(response, None)
    # If the user's choice was not found, respond saying the bot didn't understand the user's response.
    if not choice:
        not_found = await create_reply_activity(context.activity, 'Sorry, I didn\'t understand that. :(')
        await context.send_activity(not_found)
        return web.Response(status=202)
    else:
        for func in choice:
            card = func()
            response = await create_reply_activity(context.activity, '', card)
            await context.send_activity(response)
        return web.Response(status=200)


async def handle_conversation_update(context: TurnContext) -> web.Response:
    if context.activity.members_added[0].id != context.activity.recipient.id:
        response = await create_reply_activity(context.activity, 'Welcome to the Rich Cards Bot!')
        await context.send_activity(response)
    return web.Response(status=200)


async def unhandled_activity() -> web.Response:
    return web.Response(status=404)


async def request_handler(context: TurnContext) -> web.Response:
    if context.activity.type == 'message':
        return await handle_message(context)
    elif context.activity.type == 'conversationUpdate':
        return await handle_conversation_update(context)
    else:
        return await unhandled_activity()


async def messages(req: web.web_request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers['Authorization'] if 'Authorization' in req.headers else ''
    try:
        return await ADAPTER.process_activity(activity, auth_header, request_handler)
    except Exception as e:
        raise e


app = web.Application()
app.router.add_post('/', messages)

try:
    web.run_app(app, host='localhost', port=PORT)
except Exception as e:
    raise e
