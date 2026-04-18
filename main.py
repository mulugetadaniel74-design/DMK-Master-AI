@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # ለጄሚኒ ትክክለኛውን መመሪያ እና ጥያቄ መስጠት
        full_prompt = (
            f"አንተ የዳንኤል ሙሉጌታ ኩምሳ ረዳት 'DMK Master AI' ነህ። "
            f"የዳንኤል መርህ 'ሰብአዊነት ይቅደም' ነው። ሁልጊዜ በአጭር አማርኛ መልስ ስጥ።\n\n"
            f"ተጠቃሚው እንዲህ ብሏል፦ {message.text}"
        )
        
        response = model.generate_content(full_prompt)
        bot.reply_to(message, response.text)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "እባክህ ድጋሚ ጠይቀኝ፣ ትንሽ ተረባብሼ ነበር።")
        
