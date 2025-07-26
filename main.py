import logging
import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройка логов для Railway
logging.basicConfig(level=logging.INFO)

# Токен бота из переменной окружения
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# Ссылка на файл с витаминами на GitHub (RAW-ссылка!)
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
vitamin_knowledge = {}  # база знаний будет храниться здесь

# Команда: /обновить_базу — загружает JSON с GitHub
@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge
    logging.info("📥 Запрос на обновление базы витаминов...")
    async with aiohttp.ClientSession() as session:
        async with session.get(VITAMINS_URL) as resp:
            if resp.status == 200:
                text = await resp.text()
                vitamin_knowledge = json.loads(text)
                logging.info("✅ База витаминов загружена:")
                logging.info(vitamin_knowledge)
                await message.reply("✅ База витаминов успешно обновлена!")
            else:
                logging.warning(f"⚠️ Не удалось загрузить базу. Код: {resp.status}")
                await message.reply("⚠️ Не удалось загрузить базу знаний.")

# Обработка сообщений: витамин d, витамин b12 и т.п.
@dp.message_handler(lambda msg: msg.text.lower().startswith("витамин"))
async def reply_about_vitamin(message: types.Message):
    query = message.text.lower().strip()
    logging.info(f"🔍 Запрос пользователя: {query}")
    for name, info in vitamin_knowledge.items():
        if query in name.lower():
            response = f"💊 *{name}*\n"
            for key, value in info.items():
                response += f"• **{key.capitalize()}**: {value}\n"
            await message.reply(response, parse_mode="Markdown")
            return
    await message.reply("😔 Не нашёл такого витамина в базе.")

# Запуск бота
if __name__ == "__main__":
    print("🚀 Бот запущен и готов к работе!")
    executor.start_polling(dp, skip_updates=True)
