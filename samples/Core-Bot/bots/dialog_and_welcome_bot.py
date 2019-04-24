import json

from typing import List
from botbuilder.core import CardFactory
from botbuilder.core import ActivityHandler, ConversationState, UserState, TurnContext
from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity, Attachment, ChannelAccount

from .dialog_bot import DialogBot

class DialogAndWelcomeBot(DialogBot):

    def __init__(self, conversation_state: ConversationState, user_state: UserState, dialog: Dialog):
        super(DialogAndWelcomeBot, self).__init__(conversation_state, user_state, dialog)

    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            # To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards for more details.
            if member.id != turn_context.activity.recipient.id:
                welcome_card = CreateAdaptiveCardAttachment()
                response = CreateResponse(turn_context.activity, welcome_card)
                await turn_context.send_activity(response)
    
    # Create an attachment message response.
    def create_response(self, activity: Activity, attachment: Attachment):
        response = ((Activity)activity).CreateReply()
        response.Attachments = new List<Attachment>() { attachment }
        return response

    # Load attachment from file.
    def create_adaptive_card_attachment(self):
    {
        # combine path for cross platform support
        string[] paths = { ".", "Cards", "welcomeCard.json" };
        string fullPath = Path.Combine(paths);
        var adaptiveCard = File.ReadAllText(fullPath);
        return new Attachment()
        {
            ContentType = "application/vnd.microsoft.card.adaptive",
            Content = JsonConvert.DeserializeObject(adaptiveCard),
        };
    }