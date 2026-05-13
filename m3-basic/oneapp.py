import re

from aiohttp.web import Application, Request, Response, run_app
from microsoft_agents.hosting.aiohttp import (
    CloudAdapter,
    jwt_authorization_middleware,
    start_agent_process,
)
from microsoft_agents.hosting.core import (
    AgentApplication,
    AgentAuthConfiguration,
    MemoryStorage,
    TurnContext,
    TurnState,
)

AGENT_APP = AgentApplication[TurnState](
    storage=MemoryStorage(),
    adapter=CloudAdapter(),
)


@AGENT_APP.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, _: TurnState):
    await context.send_activity("Hello! How can I help you?")


@AGENT_APP.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, state: TurnState):
    for member in context.activity.members_added or []:
        if member.id != context.activity.recipient.id:
            await context.send_activity("Welcome!")


@AGENT_APP.message("/help")
async def on_help(context: TurnContext, _: TurnState):
    await context.send_activity("Here's what I can do...")


@AGENT_APP.message(re.compile(r"^order\s+\d+$", re.IGNORECASE))
async def on_order(context: TurnContext, _: TurnState):
    await context.send_activity("Looking up your order...")


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, state: TurnState):
    # Conversation scope — persisted per conversation
    count = state.conversation.get_value("message_count") or 0
    state.conversation.set_value("message_count", count + 1)

    # User scope — persisted per user
    name = state.user.get_value("display_name")

    await context.send_activity(f"Message #{count + 1}: {context.activity.text}")


if __name__ == "__main__":

    async def messages(req: Request) -> Response:
        return await start_agent_process(req, AGENT_APP, AGENT_APP.adapter)

    app = Application(middlewares=[jwt_authorization_middleware])
    app.router.add_post("/api/messages", messages)
    app.router.add_get("/api/messages", lambda _: Response(status=200))
    app["agent_configuration"] = AgentAuthConfiguration(anonymous_allowed=True)
    app["agent_app"] = AGENT_APP
    app["adapter"] = AGENT_APP.adapter
    run_app(app, host="localhost", port=3978)
