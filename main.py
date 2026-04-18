import telebot
import requests
from groq import Groq
import time
import os

# --- 1. አዲሱ መለያ ቁጥሮች ---
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ግጭትን ለመከላከል የድሮ ግንኙነትን ማጽዳት
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

SYSTEM_PROMPT = "አንተ 'DMK Master AI' የዳንኤል ረዳት ነህ። በማንኛውም ቋንቋ መልስ ስጥ። ሰብአዊነት ይቅደም!"

# --- 2. ለጽሁፍ መልእክት ---
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message.text}]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

# --- 3. ለፎቶ (Vision) ---
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "ፎቶውን እያየሁት ነው...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "ይህ ፎቶ ምን እንደሆነ በአማርኛ አብራራ።"},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "ፎቶውን ማየት አልቻልኩም።")

# --- 4. ለድምጽ (Voice) ---
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.reply_to(message, "ድምጽህን እየሰማሁ ነው...")
    try:
        file_info = bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        audio_data = requests.get(file_url).content
        
        with open("voice.ogg", "wb") as f:
            f.write(audio_data)
        
        with open("voice.ogg", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=("voice.ogg", audio_file.read()),
                model="whisper-large-v3",
                response_format="text"
            )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": transcription}]
        )
        bot.reply_to(message, f"የሰማሁት፡ {transcription}\n\nምላሽ፡ {completion.choices[0].message.content}")
    except Exception as e:
        bot.reply_to(message, "ድምጽህን መረዳት አልቻልኩም!")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
                         
