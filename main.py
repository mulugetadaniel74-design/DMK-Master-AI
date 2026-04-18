import telebot
from groq import Groq

# 1. ቁልፎቹን በቀጥታ እዚህ ጋር አስገብቻቸዋለሁ
BOT_TOKEN = "8308148615:AAHQdiHJaHarq5zaM2AiORKh26mh-F_dUTM"
GROQ_API_KEY = "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"

# 2. ቦቱን እና Groqን ማስጀመር
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# 3. ከGroq AI መልስ የሚያመጣ ፋንክሽን
def get_ai_response(user_text):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "አንተ 'DMK Master AI' የተባልክ የዳንኤል ረዳት ነህ። ሁልጊዜ በአማርኛ ጥልቀት ያለው መልስ ስጥ።"
                },
                {"role": "user", "content": user_text}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"ይቅርታ፣ ስህተት ተከስቷል፦ {e}"

# 4. መልእክት ሲመጣ የሚሰራው ክፍል
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response = get_ai_response(message.text)
    bot.reply_to(message, response)

# 5. ቦቱን ማስነሳት
if __name__ == "__main__":
    print("ቦቱ እየሰራ ነው...")
    bot.infinity_polling()
    
