import telebot
import requests
from groq import Groq
import time

# ቁልፎቹ በትክክል መሆናቸውን አረጋግጥ
BOT_TOKEN = "8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ግጭትን ለመከላከል
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

# --- AIው ስለ አንተ የሚያውቀው መረጃ ---
SYSTEM_PROMPT = """
አንተ 'DMK Master AI' የተባልክ የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ዲጂታል ረዳት ነህ። 
ስለ ዳንኤል ከተጠየቅክ የሚከተለውን መረጃ ተጠቀም፦
- ዳንኤል ሙሉጌታ ኩምሳ (DMK) በኢትዮጵያ አዲስ አበባ ውስጥ የሚኖር የሶፍትዌር ደቨሎፐር እና ፈላስፋ ነው።
- ዋና መርሁ 'ሰብአዊነት ይቅደም' (Humanity First) የሚል ነው።
- 'ማንንም አልፈራም' (Maninnem Alferam) የተባለ መጽሐፍ ደራሲ ነው።
- በአሁኑ ወቅት በቴሌግራም ላይ አርቲፊሻል ኢንተለጀንስ በማበልጸግ ላይ ይገኛል።

መመሪያ፦
1. ሁልጊዜ ዳንኤልን ወክለህ ተናገር።
2. በማንኛውም ተጠቃሚው በሚናገረው ቋንቋ (አማርኛ፣ ኦሮሚኛ፣ እንግሊዝኛ...) መልስ ስጥ።
3. ትሁት፣ አጋዥ እና ጥልቅ እውቀት ያለህ ሁን።
"""

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

# ፎቶዎችን እንዲተነትን
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "ይህንን ፎቶ ለዳንኤል አብራራለት።"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except:
        bot.reply_to(message, "ፎቶውን ማየት አልቻልኩም!")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
    
