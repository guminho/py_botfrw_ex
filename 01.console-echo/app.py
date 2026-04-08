# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio

from console_adapter import ConsoleAdapter
from echo_bot import EchoBot

ADAPTER = ConsoleAdapter()
BOT = EchoBot()


async def main():
    print("Hello and welcome!")
    await ADAPTER.process_activity(BOT.on_turn)


if __name__ == "__main__":
    asyncio.run(main())
