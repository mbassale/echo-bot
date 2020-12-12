# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, ConversationState, UserState
from botbuilder.schema import ChannelAccount

from models.user import UserProfile
from models.conversation import ConversationData


class EchoBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        if conversation_state is None:
            raise TypeError(
                "[StateManagementBot]: Missing parameter. conversation_state is required but None was given")
        if user_state is None:
            raise TypeError(
                "[StateManagementBot]: Missing parameter. user_state is required but None was given")

        self.conversation_state = conversation_state
        self.conversation_data_accessor = self.conversation_state.create_property('ConversationData')
        self.user_state = user_state

    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"You said '{turn_context.activity.text}'")

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                pass

    async def on_event_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f'Event Activity: {turn_context.activity.type}')

    async def on_turn(self, turn_context: TurnContext):
        conversation_data = await self.conversation_data_accessor.get(turn_context, ConversationData)
        if not conversation_data.did_welcome_user:
            await turn_context.send_activity("Hello! Welcome, please type something to see an amusing response!")
            conversation_data.did_welcome_user = True

        await super().on_turn(turn_context)

        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)
