# List of activity types supported by the Bot Framework. */
class ActivityType:
    # A user has added/removed the bot as a contact. */
    contactRelationUpdate = 'contactRelationUpdate'
    # User(s) have either joined or left the conversation. */
    conversationUpdate = 'conversationUpdate'
    # The conversation is being ended by either the bot or user. */
    endOfConversation = 'endOfConversation'
    # A named event sent from or to a client. */
    event = 'event'
    # An operation is being invoked. */
    invoke = 'invoke'
    # A message sent from or to a user/group. */
    message = 'message'
    # A message activity within a conversation has had a message reaction added or removed. */
    messageReaction = 'messageReaction'
    # An indicator that the bot is typing. Should be periodically resent every few seconds. */
    typing = 'typing'

# Desired layout style for a list of attachments sent to a user. */
class AttachmentLayout:
    # Attachments should be rendered as a list. */
    list = 'list'
    # Attachments should be rendered using a carousel layout. */
    carousel = 'carousel'

class CardContentType:
    hero = 'application/vnd.microsoft.card.hero'
    thumbnail = 'application/vnd.microsoft.card.thumbnail'
    receipt = 'application/vnd.microsoft.card.receipt'
    signin = 'application/vnd.microsoft.card.signin'
    animation = 'application/vnd.microsoft.card.animation'
    audio = 'application/vnd.microsoft.card.audio'
    video = 'application/vnd.microsoft.card.video'
