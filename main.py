import os
import telebot
from groq import Groq
from dotenv import load_dotenv

# .env ፋይል ውስጥ ያሉትን መረጃዎች ለመጫን
load_dotenv()

# ቁልፎችን ከ Environment Variables ላይ ማንበብ
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# ቦቱን እና Groqን ማስጀመር
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ለተጠቃሚው መልስ የሚሰጥ ፋንክሽን
def get_ai_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "አንተ ጎበዝ ረዳት ነህ።"},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"ይቅርታ፣ ችግር ተከስቷል፦ {e}"

# መልእክት ሲመጣ የሚሰራው ክፍል
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_input = message.text
    # ለተጠቃሚው "በማሰብ ላይ ነኝ..." የሚል ምልክት ለማሳየት
    bot.send_chat_action(message.chat.id, 'typing')
    
    # የAI መልሱን ማግኘት
    response = get_ai_response(user_input)
    
    # መልሱን ለተጠቃሚው መላክ
    bot.reply_to(message, response)

# ቦቱን ማስነሳት
if __name__ == "__main__":
    print("ቦቱ እየሰራ ነው...")
    bot.infinity_polling()
    
