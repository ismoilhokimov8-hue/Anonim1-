import os
import asyncio
from urllib.parse import quote
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import BufferedInputFile
from aiohttp import web, ClientSession

# Вставьте ваш НОВЫЙ токен от @BotFather в кавычки
TOKEN = "8705937681:AAEUdjyHJK5N5JpRZ4VWriGM2VfPCotN540"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция генерации картинки через ИИ (Pollinations.ai)
async def generate_ai_image(prompt: str):
    encoded_prompt = quote(prompt)
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    async with ClientSession(headers=headers) as session:
        async with session.get(image_url, timeout=30) as resp:
            if resp.status == 200:
                return await resp.read()
    return None

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "🎨 **Привет! Я ИИ-Художник.**\n\n"
        "Напиши мне любое описание картинки (например: *«красивый котик в космосе, неоновый стиль»*), и я сгенерирую для тебя изображение!",
        parse_mode="Markdown"
    )

@dp.message()
async def generate_handler(message: types.Message):
    prompt = message.text or ""
    
    if len(prompt) < 3:
        await message.answer("⚠️ Пожалуйста, напишите более подробное описание для картинки.")
        return

    msg = await message.answer("🎨 **Генерирую картинку с помощью ИИ...**\nЭто займет около 5-10 секунд.")

    try:
        image_bytes = await generate_ai_image(prompt)
        if image_bytes:
            photo = BufferedInputFile(image_bytes, filename="ai_art.jpg")
            await message.answer_photo(photo=photo, caption=f"🖼 **Результат по запросу:**\n_{prompt}_", parse_mode="Markdown")
            await msg.delete()
        else:
            await msg.edit_text("❌ Не удалось сгенерировать картинку. Попробуйте еще раз.")
    except Exception:
        await msg.edit_text("❌ Ошибка при генерации. Попробуйте сформулировать запрос иначе.")

async def handle_ping(request):
    return web.Response(text="AI Bot is running 24/7!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

    
