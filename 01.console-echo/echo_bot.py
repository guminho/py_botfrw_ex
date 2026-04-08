from sys import exit

from botbuilder.core import TurnContext


class EchoBot:
    async def on_turn(self, turn_context: TurnContext):
        # Check to see if this activity is an incoming message.
        if turn_context.activity.type == "message" and turn_context.activity.text:
            if turn_context.activity.text.lower() == "quit":
                await turn_context.send_activity("Bye!")
                exit(0)
            else:
                await turn_context.send_activity(f"Echo: {turn_context.activity.text}")
