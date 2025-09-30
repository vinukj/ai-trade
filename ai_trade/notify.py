import config
from telegram import Bot  # noqa: E0401  # type: ignore
import asyncio  # add asyncio for coroutine handling


def send_telegram(message: str) -> None:
    """
    Send a message to the configured Telegram chat.
    """
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    # run the async send_message coroutine to avoid un-awaited coroutine warning
    asyncio.run(
        bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=message,
            parse_mode="Markdown"
        )
    )
