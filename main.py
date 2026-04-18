import telebot
from groq import Groq

# 1. መለያ ቁጥሮች (እነዚህን እንዳትቀይራቸው)
BOT_TOKEN = "8308148615:AAEmQF9X5Em8Kf7nOFPo1oOzJULjCnttmRI"
GROQ_API_KEY = "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"

# 2. ቦቱን እና AI ሞዴሉን ማገናኘት
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# 3. ለ AI የሚሰጥ መመሪያ (ለሁሉም ቋንቋ እና ለማንነት)
SYSTEM_PROMPT = """
አንተ 'DMK Master AI' የተባልክ የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ዲጂታል ረዳት ነህ። 
የዳንኤልን ፍልስፍናዎች፣ በተለይም 'ሰብአዊነት ይቅደም' (Humanity First) የሚለውን መርህ ታንጸባርቃለህ።
ደንቦች፦
1. ተጠቃሚው በሚያናግርህ በማንኛውም ቋንቋ መልስ ስጥ (አማርኛ፣ ኦሮሚኛ፣ እንግሊዝኛ ወዘተ)።
2. ንግግርህ ትሁት፣ ጥልቀት ያለው እና አጋዥ ይሁን።
3. ስለ ራስህ ማንነት ከተጠየቅክ የዳንኤል (DMK) ረዳት መሆንህን ንገራቸው።
"""

def get_ai_response(user_text):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"ይቅርታ ስህተት ተከስቷል፦ {e}"

# 4. መልእክት ሲመጣ የሚሰራው ክፍል
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # ቦቱ "እየጻፈ ነው..." የሚል ምልክት እንዲያሳይ
    bot.send_chat_action(message.chat.id, 'typing')
    
    # መልሱን አምጥቶ መላክ
    response = get_ai_response(message.text)
    bot.reply_to(message, response)

# 5. ቦቱን ማስነሳት
if __name__ == "__main__":
    print("DMK Master AI አሁን ዝግጁ ነው!")
    bot.infinity_polling()
    
