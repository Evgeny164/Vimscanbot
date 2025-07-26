import logging
import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Telegram токен
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# URL на vitamins.json с GitHub
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
vitamin_knowledge = {}  # здесь будет загруженная база

# Команда: обновить базу из GitHub
@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge
    async with aiohttp.ClientSession() as session:
        async with session.get(VITAMINS_URL) as resp:
            if resp.status == 200:
                data = await resp.text()
                vitamin_knowledge = json.loads(data)
                await message.reply("✅ База витаминов обновлена!")
            else:
                await message.reply("⚠️ Ошибка загрузки базы.")

# Обработка сообщений: витамин D / витамин B12 и т.п.
@dp.message_handler(lambda msg: msg.text.lower().startswith("витамин"))
async def reply_about_vitamin(message: types.Message):
    query = message.text.lower()
    for name, info in vitamin_knowledge.items():
        if name.lower() in query:
            reply = f"💊 *{name}*\n"
            for key, value in info.items():
                reply += f"• **{key.capitalize()}**: {value}\n"
            await message.reply(reply, parse_mode="Markdown")
            return
    await message.reply("Не нашёл такого витамина 😔")

# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True) 
