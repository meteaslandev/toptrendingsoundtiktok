import logging
from aiogram import Bot, Dispatcher, types
import aiohttp
import asyncio

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_API_KEY' with your actual TikTok API key
api_key = 'YOUR_API_KEY'

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = 'YOUR_BOT_TOKEN'

# Replace 'YOUR_CHAT_ID' with your actual channel chat ID
chat_id = 'YOUR_CHAT_ID'

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

async def start(message: types.Message):
    await message.answer("Bot is up and running!")

async def trending_sounds():
    url = f'https://api.tiktok.com/aweme/v1/music/trending/?key={api_key}'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    trending_sounds = data['music_list'][:50]
                    
                    sound_list = ""
                    for sound in trending_sounds:
                        sound_list += sound['title'] + "\n"
                        await asyncio.sleep(1)  # Wait for 1 second before the next request / You can edit this area as you wish to avoid being exposed to any TikTok restrictions when using the bot multiple times.
                    
                    await bot.send_message(chat_id=chat_id, text=sound_list)
                else:
                    logger.error('Error occurred while fetching trending sounds')
                    await bot.send_message(chat_id=chat_id, text='Error occurred while fetching trending sounds')
        except Exception as e:
            logger.error(f'Error occurred while fetching trending sounds: {e}')
            await bot.send_message(chat_id=chat_id, text=f'Error occurred while fetching trending sounds: {e}')

async def hello(message: types.Message):
    await message.answer("Hello, I am the bot that will list the daily trending sounds on TikTok for you.")

dp.register_message_handler(start, commands=['start'])
dp.register_message_handler(hello, commands=['hello'])

async def on_startup(dp):
    await bot.send_message(chat_id=chat_id, text='Bot has been started')

async def on_shutdown(dp):
    await bot.send_message(chat_id=chat_id, text='Bot has been stopped')

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)