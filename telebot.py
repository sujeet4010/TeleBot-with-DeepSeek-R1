import asyncio
import logging
import sys
import os

from langchain_community.llms import Ollama
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


class Reference:
    """
    A class to store previously conversation
    """
    def __init__(self) -> None:
        self.response = ""
        
load_dotenv()
TOKEN = os.getenv("TOKEN")
reference = Reference()

llm=Ollama(model='deepseek-r1:7b')

def clear_past():
    """
    This function is to clear the previous conversation and context
    """
    reference.response=""


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command('clear'))
async def clear(message: Message) -> None:
    clear_past()
    await message.reply("I've cleared the past conversation and context")

@dp.message(Command('help'))
async def clear(message: Message) -> None:
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

@dp.message()
async def deepseek_chat(message:Message):
    """
    A handler to process the user's input and generate a response using DeepSeek R1 (via Ollama).
    """
    print(f">>> USER: \n\t{message.text}")

    # Generate response using DeepSeek
    response = llm.invoke(message.text)

    print(f">>> DeepSeek R1: \n\t{response}")
    # await message.answer(chat_id=message.chat.id, text=response)
    await message.answer(response)

async def main() -> None: 
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())