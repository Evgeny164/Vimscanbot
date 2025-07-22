
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import os

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.reply("Привет! Я VIMscanBot. Пришли мне PDF, DOCX или Excel с данными пациента.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
