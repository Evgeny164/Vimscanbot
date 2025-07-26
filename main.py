Евгений Ефремов, [26.07.2025 20:59]
{
  "витамин D": {
    "роль": "Регуляция иммунитета и метаболизма кальция",
    "цель": "25(OH)D = 50–80 нг/мл",
    "дефицит": "слабость, частые инфекции, усталость",
    "формы": "D3 + K2 (МК-7)",
    "дозировка": "2000–5000 МЕ/сут"
  },
  "витамин B12": {
    "роль": "Кроветворение, нервная система",
    "анализы": "B12, гомоцистеин, MMA",
    "формы": "метилкобаламин, аденозилкобаламин",
    "дозировка": "500–1000 мкг в день"
  }
}

Евгений Ефремов, [26.07.2025 21:17]
{
  "магний": {
    "роль": "Антистресс, регуляция нервной системы и мышечного тонуса",
    "анализы": "Mg в сыворотке, RBC магний, кальций/магний",
    "дефицит": "судороги, тревожность, ПМС, запоры",
    "дозировка": "300–600 мг/сут (цитрат, малат, глицинат)"
  },
  "цинк": {
    "роль": "Иммунитет, регенерация кожи, репродуктивная функция",
    "анализы": "цинк в плазме, соотношение Zn/Cu",
    "дефицит": "акне, выпадение волос, частые инфекции",
    "дозировка": "15–30 мг/сут (пиколинат, цитрат)"
  },
  "железо": {
    "роль": "Гемоглобин, транспорт кислорода, энергия",
    "анализы": "ОЖСС, ферритин, сывороточное железо",
    "дефицит": "анемия, слабость, выпадение волос",
    "дозировка": "20–60 мг/сут (бисглицинат, сульфат)"
  },
  "йод": {
    "роль": "Щитовидная железа, синтез гормонов Т3 и Т4",
    "анализы": "йод в моче, ТТГ, Т4св, Т3св",
    "дефицит": "усталость, зябкость, узлы в ЩЖ",
    "дозировка": "150–250 мкг/сут (калия йодид, ламинария)"
  },
  "селен": {
    "роль": "Антиоксидант, щитовидка, иммунитет",
    "анализы": "Se в сыворотке, GPx",
    "дефицит": "выпадение волос, слабость, аутоиммунитет",
    "дозировка": "100–200 мкг/сут (селенометионин)"
  }
}

Евгений Ефремов, [26.07.2025 21:37]
import logging
import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Telegram токен
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# Ссылки на GitHub базы
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
MINERALS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/minerals.json"

vitamin_knowledge = {}
mineral_knowledge = {}

# Команда: /обновить_базу
@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge, mineral_knowledge
    async with aiohttp.ClientSession() as session:
        async with session.get(VITAMINS_URL) as resp1:
            if resp1.status == 200:
                text = await resp1.text()
                vitamin_knowledge = json.loads(text)
        async with session.get(MINERALS_URL) as resp2:
            if resp2.status == 200:
                text = await resp2.text()
                mineral_knowledge = json.loads(text)
    await message.reply("✅ База витаминов и минералов загружена!")

# Обработка всех сообщений
@dp.message_handler()
async def handle_query(message: types.Message):
    query = message.text.lower().strip()
    logging.info(f"🔍 User asked: {query}")

    # Поиск в витаминах
    for name, info in vitamin_knowledge.items():
        if query in name.lower():
            response = f"💊 *{name}*\n"
            for k, v in info.items():
                response += f"• **{k.capitalize()}**: {v}\n"
            await message.reply(response, parse_mode="Markdown")
            return

    # Поиск в минералах
    for name, info in mineral_knowledge.items():
        if query in name.lower():
            response = f"🧪 *{name}*\n"
            for k, v in info.items():
                response += f"• **{k.capitalize()}**: {v}\n"
            await message.reply(response, parse_mode="Markdown")
            return

    await message.reply("😔 Не нашёл такого витамина или минерала в базе.")

# Запуск бота
if __name__ == "__main__":
    print("🚀 Бот запущен!")
    executor.start_polling(dp, skip_updates=True)
