import os
import re
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web, ClientSession

# Вставьте сюда ваш НОВЫЙ токен от @BotFather
TOKEN = os.getenv("BOT_TOKEN", "8705937681:AAEUdjyHJK5N5JpRZ4VWriGM2VfPCotN540")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция получения видео без водяного знака
async def get_tiktok_video(url: str):
    api_url = "https://www.tikwm.com/api/"
    data = {"url": url, "hd": 1}
    async with ClientSession() as session:
        async with session.post(api_url, data=data) as resp:
            res = await resp.json()
            if res.get("code") == 0 and "data" in res:
                return res["data"].get("play")
    return None

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("👋 Привет! Отправь мне ссылку на видео из TikTok, и я скачаю его без водяного знака!")

@dp.message()
async def download_handler(message: types.Message):
    text = message.text or ""
    match = re.search(r'https?://[^\s]+', text)
    if not match or ("tiktok.com" not in text and "vt.tiktok.com" not in text):
        await message.answer("⚠️ Пожалуйста, отправьте корректную ссылку на видео из TikTok!")
        return

    tiktok_url = match.group(0)
    msg = await message.answer("⏳ Скачиваю видео, подождите...")

    try:
        video_url = await get_tiktok_video(tiktok_url)
        if video_url:
            await message.answer_video(video=video_url, caption="🎬 Вот ваше видео без водяного знака!")
            await msg.delete()
        else:
            await msg.edit_text("❌ Не удалось получить видео. Проверьте ссылку или попробуйте позже.")
    except Exception as e:
        await msg.edit_text("❌ Произошла ошибка при загрузке видео.")

async def handle_ping(request):
    return web.Response(text="Bot is running 24/7!")

async def main():
    # Фейковый веб-сервер для поддержки Render Web Service
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    # Сброс возможных зависших сессий и запуск
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
          
