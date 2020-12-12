from typing import Callable, Awaitable
from botbuilder.core import Middleware, TurnContext

from models.user import UserProfile


class LoginMiddleware(Middleware):
    # noinspection PyShadowingBuiltins
    async def on_turn(self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]):
        context_user_id = context.activity.from_property.id
        if context_user_id.isdigit():
            await context.send_activity(f'Valid UserId: {context_user_id}')
            user_profile = UserProfile()
            user_profile.user_id = context_user_id
            context.turn_state['user_profile'] = user_profile
            await logic()
