# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime, timedelta
from threading import Lock

from botbuilder.core import BotStateSet, ConversationState, UserState, TurnContext
from botbuilder.dialogs.memory import DialogStateManagerConfiguration

from .dialog import Dialog
from .dialog_context import DialogContext
from .dialog_set import DialogSet
from .dialog_state import DialogState
from .dialog_manager_result import DialogManagerResult

# <summary>
# Class which runs the dialog system.
# </summary>
class DialogManager:

    # <summary>
    # Initializes a instance of the <see cref="DialogManager"/> class.
    # </summary>
    # <param name="root_dialog">Root dialog to use.</param>
    # <param name="dialog_state_property">alternate name for the dialog_state property. (Default is "DialogState").</param>
    def __init__(self, root_dialog: Dialog = None, dialog_state_property: str = None):
        self.last_access = "_lastAccess"
        self._root_dialog_id = ""
        self._dialog_state_property = dialog_state_property or "DialogState"
        self._lock = Lock()
        self.root_dialog = root_dialog
        # <summary>
        # Gets or sets the ConversationState.
        # </summary>
        # <value>
        # The ConversationState.
        # </value>
        self.conversation_state: ConversationState = None

        # <summary>
        # Gets or sets the UserState.
        # </summary>
        # <value>
        # The UserState.
        # </value>
        self.user_state: UserState = None

        # <summary>
        # Gets InitialTurnState collection to copy into the TurnState on every turn.
        # </summary>
        # <value>
        # TurnState.
        # </value>
        self.initial_turn_state = {}

        # <summary>
        # Gets or sets root dialog to use to start conversation.
        # </summary>
        # <value>
        # Root dialog to use to start conversation.
        # </value>
        self.root_dialog: Dialog = None

        # <summary>
        # Gets or sets global dialogs that you want to have be callable.
        # </summary>
        # <value>Dialogs set.</value>
        self.dialogs = DialogSet()

        # <summary>
        # Gets or sets the DialogStateManagerConfiguration.
        # </summary>
        # <value>
        # The DialogStateManagerConfiguration.
        # </value>
        self.state_configuration: DialogStateManagerConfiguration = None

        # <summary>
        # Gets or sets (optional) number of milliseconds to expire the bot's state after.
        # </summary>
        # <value>
        # Number of milliseconds.
        # </value>
        self.expire_after: int = None

    # <summary>
    # Runs dialog system in the context of an ITurnContext.
    # </summary>
    # <param name="context">turn context.</param>
    # <param name="cancellationToken">Cancellation token.</param>
    # <returns>result of the running the logic against the activity.</returns>
    async def on_turn(self, context: TurnContext) -> DialogManagerResult:
        # Lazy initialize RootDialog so it can refer to assets like LG function templates
        if self._root_dialog_id is None:
            with self._lock:
                if self._root_dialog_id is None:
                    self._root_dialog_id = self.root_dialog.id
                    #self.dialogs = self.root_dialog.telemetry_client
                    self.dialogs.add(self.root_dialog)

        bot_state_set = BotStateSet()

        # Preload TurnState with DM TurnState.
        for key, val in self.initial_turn_state:
            context.turn_state[key] = val
    
        # register DialogManager with TurnState.
        context.turn_state[DialogManager.__class__.__name__] = self
        conversation_state_name = ConversationState.__class__.__name__
        if self.conversation_state is None:
            if conversation_state_name not in context.turn_state:
                raise Exception(f"Unable to get an instance of {conversation_state_name} from turn_context.")
            self.conversation_state: ConversationState = context.turn_state[conversation_state_name]
        else:
            context.turn_state[conversation_state_name] = self.conversation_state
    
        bot_state_set.add(self.conversation_state)

        user_state_name = UserState.__class__.__name__
        if self.user_state is None:
            self.user_state = context.turn_state.get(user_state_name, None)
        else:
            context.turn_state[user_state_name] = self.user_state
    
        if self.user_state is not None:
            self.user_state: UserState = self.user_state
            bot_state_set.add(self.user_state)
    
        # create property accessors
        # <DateTime>(last_access)
        last_access_property = self.conversation_state.create_property(self.last_access)
        last_access: datetime = await last_access_property.get(context, lambda: datetime.now())

        # Check for expired conversation
        if self.expire_after is not None and (datetime.now() - last_access) >= timedelta(milliseconds=float(self.expire_after)):
            # Clear conversation state
            await self.conversation_state.clear_state(context)
    
        last_access = datetime.now()
        await last_access_property.set(context, last_access)

        # get dialog stack 
        dialogs_property = self.conversation_state.create_property(self._dialog_state_property)
        dialog_state: DialogState = await dialogs_property.get(context, lambda: DialogState())

        # Create DialogContext
        dialog_context = DialogContext(self.dialogs, context, dialog_state)

        # promote initial TurnState into dialog_context.services for contextual services
        for key, service in dialog_context.services:
                    dialog_context.services[key] = service
    
        # map TurnState into root dialog context.services
        for key, service in  context.turn_state:
                    dialog_context.services[key] = service
    
        # get the DialogStateManager configuration
        dialog_state_manager = DialogStateManager(dialog_context, StateConfiguration)
        await dialog_state_manager.LoadAllScopesAsync(cancellationToken)
        dialog_context.Context.TurnState.Add(dialog_state_manager)

        DialogTurnResult turnResult = None

        # Loop as long as we are getting valid OnError handled we should continue executing the actions for the turn.
        //
        # NOTE: We loop around this block because each pass through we either complete the turn and break out of the loop
        # or we have had an exception AND there was an OnError action which captured the error.  We need to continue the 
        # turn based on the actions the OnError handler introduced.
        endOfTurn = false
        while (!endOfTurn)
                    try
                            if (context.TurnState.Get<IIdentity>(BotAdapter.BotIdentityKey) is ClaimsIdentity claimIdentity && SkillValidation.IsSkillClaim(claimIdentity.Claims))
                                    # The bot is running as a skill.
                    turnResult = await HandleSkillOnTurnAsync(dialog_context, cancellationToken)
                                else
                                    # The bot is running as root bot.
                    turnResult = await HandleBotOnTurnAsync(dialog_context, cancellationToken)
            
                # turn successfully completed, break the loop
                endOfTurn = true
                        catch (Exception err)
                            # fire error event, bubbling from the leaf.
                handled = await dialog_context.EmitEventAsync(DialogEvents.Error, err, bubble: true, fromLeaf: true, cancellationToken: cancellationToken)

                if (!handled)
                                    # error was NOT handled, throw the exception and end the turn. (This will trigger the Adapter.OnError handler and end the entire dialog stack)
                    throw
                                
        # save all state scopes to their respective botState locations.
        await dialog_state_manager.SaveAllChangesAsync(cancellationToken)

        # save BotState changes
        await bot_state_set.SaveAllChangesAsync(dialog_context.Context, false, cancellationToken)

        return DialogManagerResult { TurnResult = turnResult }

    # <summary>
    # Helper to send a trace activity with a memory snapshot of the active dialog DC. 
    # </summary>
    static async Task SendStateSnapshotTraceAsync(DialogContext dialog_context, str traceLabel, CancellationToken cancellationToken)
            # send trace of memory
        snapshot = GetActiveDialogContext(dialog_context).State.GetMemorySnapshot()
        traceActivity = (Activity)Activity.CreateTraceActivity("BotState", "https://www.botframework.com/schemas/botState", snapshot, traceLabel)
        await dialog_context.Context.SendActivityAsync(traceActivity, cancellationToken)

    static bool IsFromParentToSkill(ITurnContext turnContext)
            if (turnContext.TurnState.Get<SkillConversationReference>(SkillHandler.SkillConversationReferenceKey) != None)
                    return false
    
        return turnContext.TurnState.Get<IIdentity>(BotAdapter.BotIdentityKey) is ClaimsIdentity claimIdentity && SkillValidation.IsSkillClaim(claimIdentity.Claims)

    # Recursively walk up the DC stack to find the active DC.
    static DialogContext GetActiveDialogContext(DialogContext dialogContext)
            child = dialogContext.Child
        if (childis None)
                    return dialogContext
    
        return GetActiveDialogContext(child)

    # <summary>
    # Helper to determine if we should send an EndOfConversation to the parent or not.
    # </summary>
    static bool ShouldSendEndOfConversationToParent(ITurnContext context, DialogTurnResult turnResult)
            if (!(turnResult.Status == DialogTurnStatus.Complete || turnResult.Status == DialogTurnStatus.Cancelled))
                    # The dialog is still going, don't return EoC.
            return false
    
        if (context.TurnState.Get<IIdentity>(BotAdapter.BotIdentityKey) is ClaimsIdentity claimIdentity && SkillValidation.IsSkillClaim(claimIdentity.Claims))
                    # EoC Activities returned by skills are bounced back to the bot by SkillHandler.
            # In those cases we will have a SkillConversationReference instance in state.
            skillConversationReference = context.TurnState.Get<SkillConversationReference>(SkillHandler.SkillConversationReferenceKey)
            if (skillConversationReference != None)
                            # If the skillConversationReference.OAuthScope is for one of the supported channels, we are at the root and we should not send an EoC.
                return skillConversationReference.OAuthScope != AuthenticationConstants.ToChannelFromBotOAuthScope && skillConversationReference.OAuthScope != GovernmentAuthenticationConstants.ToChannelFromBotOAuthScope
        
            return true
    
        return false

    async Task<DialogTurnResult> HandleSkillOnTurnAsync(DialogContext dialog_context, CancellationToken cancellationToken)
            # the bot is running as a skill. 
        turnContext = dialog_context.Context

        # Process remote cancellation
        if (turnContext.Activity.Type == ActivityTypes.EndOfConversation && dialog_context.ActiveDialog != None && IsFromParentToSkill(turnContext))
                    # Handle remote cancellation request from parent.
            activeDialogContext = GetActiveDialogContext(dialog_context)

            remoteCancelText = "Skill was canceled through an EndOfConversation activity from the parent."
            await turnContext.TraceActivityAsync($"{GetType().Name}.OnTurnAsync()", label: $"{remoteCancelText}", cancellationToken: cancellationToken)

            # Send cancellation message to the top dialog in the stack to ensure all the parents are canceled in the right order. 
            return await activeDialogContext.CancelAllDialogsAsync(true, cancellationToken: cancellationToken)
    
        # Handle reprompt
        # Process a reprompt event sent from the parent.
        if (turnContext.Activity.Type == ActivityTypes.Event && turnContext.Activity.Name == DialogEvents.RepromptDialog)
                    if (dialog_context.ActiveDialogis None)
                            return DialogTurnResult(DialogTurnStatus.Empty)
        
            await dialog_context.RepromptDialogAsync(cancellationToken)
            return DialogTurnResult(DialogTurnStatus.Waiting)
    
        # Continue execution
        # - This will apply any queued up interruptions and execute the current/next step(s).
        turnResult = await dialog_context.ContinueDialogAsync(cancellationToken)
        if (turnResult.Status == DialogTurnStatus.Empty)
                    # restart root dialog
            startMessageText = $"Starting {_root_dialog_id}."
            await turnContext.TraceActivityAsync($"{GetType().Name}.OnTurnAsync()", label: $"{startMessageText}", cancellationToken: cancellationToken)
            turnResult = await dialog_context.BeginDialogAsync(_root_dialog_id, cancellationToken: cancellationToken)
    
        await SendStateSnapshotTraceAsync(dialog_context, "Skill State", cancellationToken)

        if (ShouldSendEndOfConversationToParent(turnContext, turnResult))
                    endMessageText = $"Dialog {_root_dialog_id} has **completed**. Sending EndOfConversation."
            await turnContext.TraceActivityAsync($"{GetType().Name}.OnTurnAsync()", label: $"{endMessageText}", value: turnResult.Result, cancellationToken: cancellationToken)

            # Send End of conversation at the end.
            activity = Activity(ActivityTypes.EndOfConversation)
                            Value = turnResult.Result,
                Locale = turnContext.Activity.Locale
                        await turnContext.SendActivityAsync(activity, cancellationToken)
    
        return turnResult

    async Task<DialogTurnResult> HandleBotOnTurnAsync(DialogContext dialog_context, CancellationToken cancellationToken)
            DialogTurnResult turnResult

        # the bot is running as a root bot. 
        if (dialog_context.ActiveDialogis None)
                    # start root dialog
            turnResult = await dialog_context.BeginDialogAsync(_root_dialog_id, cancellationToken: cancellationToken)
                else
                    # Continue execution
            # - This will apply any queued up interruptions and execute the current/next step(s).
            turnResult = await dialog_context.ContinueDialogAsync(cancellationToken)

            if (turnResult.Status == DialogTurnStatus.Empty)
                            # restart root dialog
                turnResult = await dialog_context.BeginDialogAsync(_root_dialog_id, cancellationToken: cancellationToken)
                
        await SendStateSnapshotTraceAsync(dialog_context, "Bot State", cancellationToken)

        return turnResult
