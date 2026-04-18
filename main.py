import telebot
from groq import Groq

# 1. አዲሱ ቶክን እና የGroq ቁልፍ (ምንም ክፍተት እንዳይኖር ተጠንቀቅ)
BOT_TOKEN = "8308148615:AAEmQF9X5Em8Kf7nOFPo1oOzJULjCnttmRI"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # ቦቱ "እየጻፈ ነው..." የሚል ምልክት እንዲያሳይ
        bot.send_chat_action(message.chat.id, 'typing')
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "አንተ የዳንኤል ረዳት DMK AI ነህ።"},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"ይቅርታ ስህተት ተከስቷል፦ {e}")

if __name__ == "__main__":
    print("ቦቱ እየሰራ ነው...")
    bot.infinity_polling()
    
