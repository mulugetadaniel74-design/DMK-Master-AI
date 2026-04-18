import os
import telebot
from groq import Groq
from dotenv import load_dotenv

# 1. Environment Variables መጫን (ለአካባቢው ፋይል)
load_dotenv()

# 2. ቁልፎችን ከ Render Environment Variables ማግኘት
# Render ላይ BOT_TOKEN እና GROQ_API_KEY ብለህ መመዝገብህን አረጋግጥ
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# 3. ቦቱን እና Groqን ማስጀመር
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# 4. ከGroq AI መልስ የሚያመጣ ፋንክሽን
def get_ai_response(user_text):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "አንተ 'DMK Master AI' የተባልክ የዳንኤል ረዳት ነህ። ሁልጊዜ በአማርኛ ጥልቀት ያለው እና ግልጽ መልስ ስጥ።"
                },
                {"role": "user", "content": user_text}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"ይቅርታ ዳንኤል፣ የAI ስህተት ተከስቷል፦ {e}"

# 5. መልእክት ሲመጣ የሚሰራው ክፍል
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # ቦቱ "እየጻፈ ነው..." የሚል ምልክት እንዲያሳይ
    bot.send_chat_action(message.chat.id, 'typing')
    
    # መልሱን ከGroq AI አምጥቶ መላክ
    response = get_ai_response(message.text)
    bot.reply_to(message, response)

# 6. ቦቱን ማስነሳት
if __name__ == "__main__":
    print("ቦቱ በተሳካ ሁኔታ ተነስቷል!")
    bot.infinity_polling()
    
