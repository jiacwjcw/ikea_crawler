import asyncio

import telegram

from configs import SETTINGS

TOKEN = SETTINGS.telegram.token
CHAT_ID = SETTINGS.telegram.chat_id


def send(msg):
    bot = telegram.Bot(token=TOKEN)
    asyncio.run(bot.sendMessage(chat_id=CHAT_ID, text=msg))


if __name__ == "__main__":
    text = """@<user> 巴黎巴黎"""
    send(text)
