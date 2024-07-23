import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 챗GPT API 키
GPT_API_KEY=${{ secrets.GPT_API_KEY }}
# 텔레그램 봇 토큰
TELEGRAM_TOKEN=${{ secrets.TELEGRAM_TOKEN }}

async def get_gpt_response(prompt, api_key):
    print("Requesting GPT-4 API...")  # 디버깅용 로그 출력
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4',
        'messages': [{"role": "user", "content": prompt}]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    print("Received response from GPT-4 API.")  # 디버깅용 로그 출력
    response_json = response.json()
    print(response_json)  # 응답 전체를 출력하여 확인
    if "choices" in response_json:
        return response_json['choices'][0]['message']['content'].strip()
    else:
        print("Error in response:", response_json)  # 에러 내용 출력
        return "Sorry, I couldn't process your request. Please try again later."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, Gunner😀 뭘 도와줄까?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"Received message: {user_message}")  # 디버깅용 로그 출력
    response = await get_gpt_response(user_message, GPT_API_KEY)
    await update.message.reply_text(response)

def main():
    print("Starting bot...")  # 디버깅용 로그 출력
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started. Running polling...")  # 디버깅용 로그 출력
    application.run_polling()

if __name__ == '__main__':
    main()
