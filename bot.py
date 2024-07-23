import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# 챗GPT API 키
GPT_API_KEY = os.getenv('GPT_API_KEY')
# 텔레그램 봇 토큰
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

def get_gpt_response(prompt, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',  # 모델명
        'messages': [{"role": "user", "content": prompt}],  # 대화 형식
        'max_tokens': 150
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    return response.json()['choices'][0]['message']['content'].strip()

def start(update, context):
    update.message.reply_text('Hello, Gunner😀 뭘 도와줄까?')

def handle_message(update, context):
    user_message = update.message.text
    response = get_gpt_response(user_message, GPT_API_KEY)
    update.message.reply_text(response)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
