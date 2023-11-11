from telegram.ext import Updater, CommandHandler
import requests

# Replace 'YOUR_API_KEY' with your actual TikTok API key
api_key = 'YOUR_API_KEY'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is up and running!")

def trending_sounds(update, context):
    url = f'https://api.tiktok.com/aweme/v1/music/trending/?key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        trending_sounds = data['music_list'][:50]
        
        sound_list = ""
        for sound in trending_sounds:
            sound_list += sound['title'] + "\n"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=sound_list)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Error occurred while fetching trending sounds')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
trending_sounds_handler = CommandHandler('trendingsounds', trending_sounds)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(trending_sounds_handler)

updater.start_polling()
