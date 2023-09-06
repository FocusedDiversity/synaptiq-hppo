import asyncio

from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp


async def init_slack_bot(bot_token: str, signing_secret: str, app_token: str):
    app = AsyncApp(token=bot_token, signing_secret=signing_secret)

    @app.event("message")
    async def event_im_message(event, say):
        user = event["user"]
        await say(
            f"Hi there {user}! I'm not yet configured to do anything but say 'Hi there!'"
        )

    handler = AsyncSocketModeHandler(app=app, app_token=app_token)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(init_slack_bot())
