import telebot
import google.generativeai as genai

bot = telebot.TeleBot("8308148615:AAHBvWtd8ondkVQiebRxHADRa2KCB5b1wPg")
genai.configure(api_key="AIzaSyDZafdaUpR5SJDFBi4DBbC72q_GwCk5P-c")
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"ስህተት ተፈጥሯል፡ {e}")

bot.infinity_polling()
