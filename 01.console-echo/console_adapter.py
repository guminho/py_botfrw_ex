# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import datetime
from typing import Callable

from botbuilder.core.bot_adapter import BotAdapter
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
    ConversationReference,
    ResourceResponse,
)


class ConsoleAdapter(BotAdapter):
    """
    Lets a user communicate with a bot from a console window.

    :Example:
    async def logic(context):
        await context.send_activity('Hello World!')

    adapter = ConsoleAdapter()
    adapter.process_activity(logic))
    ...
    """

    def __init__(self):
        super(ConsoleAdapter, self).__init__()

        self.reference = ConversationReference(
            channel_id="console",
            user=ChannelAccount(id="user", name="User1"),
            bot=ChannelAccount(id="bot", name="Bot"),
            conversation=ConversationAccount(id="convo1", name="", is_group=False),
            service_url="",
        )

        self._next_id = 0

    async def process_activity(self, logic: Callable):
        """
        Begins listening to console input.
        :param logic:
        :return:
        """
        while True:
            msg = input()
            if msg is None:
                pass
            else:
                self._next_id += 1
                activity = Activity(
                    text=msg,
                    channel_id="console",
                    from_property=ChannelAccount(id="user", name="User1"),
                    recipient=ChannelAccount(id="bot", name="Bot"),
                    conversation=ConversationAccount(id="Convo1"),
                    type=ActivityTypes.message,
                    timestamp=datetime.datetime.now(),
                    id=str(self._next_id),
                )

                activity = TurnContext.apply_conversation_reference(
                    activity, self.reference, True
                )
                context = TurnContext(self, activity)
                await self.run_pipeline(context, logic)

    async def send_activities(
        self, context: TurnContext, activities: list[Activity]
    ) -> list[ResourceResponse]:
        """
        Logs a series of activities to the console.
        :param context:
        :param activities:
        :return:
        """
        if context is None:
            raise TypeError(
                "ConsoleAdapter.send_activities(): `context` argument cannot be None."
            )
        if not isinstance(activities, list):
            raise TypeError(
                "ConsoleAdapter.send_activities(): `activities` argument must be a list."
            )
        if len(activities) == 0:
            raise ValueError(
                "ConsoleAdapter.send_activities(): `activities` argument cannot have a length of 0."
            )

        async def next_activity(i: int):
            responses = []

            if i < len(activities):
                responses.append(ResourceResponse())
                activity = activities[i]

                if activity.type == "delay":
                    await asyncio.sleep(activity.delay)
                    await next_activity(i + 1)
                elif activity.type == ActivityTypes.message:
                    if (
                        activity.attachments is not None
                        and len(activity.attachments) > 0
                    ):
                        append = (
                            "(1 attachment)"
                            if len(activity.attachments) == 1
                            else f"({len(activity.attachments)} attachments)"
                        )
                        print(f"{activity.text} {append}")
                    else:
                        print(activity.text)
                    await next_activity(i + 1)
                else:
                    print(f"[{activity.type}]")
                    await next_activity(i + 1)
            else:
                return responses

        await next_activity(0)

    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        raise NotImplementedError()

    async def update_activity(self, context: TurnContext, activity: Activity):
        raise NotImplementedError()
