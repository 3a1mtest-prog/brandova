@bot.message_handler(commands=['start'])
def start(message):
    # إنشاء الكيبورد وتفعيله بحيث يظهر كخيار وحيد
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_ar = types.KeyboardButton("العربية 🇸🇦")
    btn_en = types.KeyboardButton("English 🇺🇸")
    markup.add(btn_ar, btn_en)
    
    # إرسال الرسالة مع إرفاق الكيبورد (هذا هو الجزء الذي كان ينقصك)
    bot.send_message(message.chat.id, "يرجى اختيار اللغة / Please choose your language", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["العربية 🇸🇦", "English 🇺🇸"])
def language_selection(message):
    if message.text == "العربية 🇸🇦":
        welcome_msg = "أهلاً بك في شركة برندوفا BRANDOFA! 🚀\nيسعدنا مساعدتك، اضغط على 'ابدأ' لنبدأ العمل."
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("ابدأ العمل ⚡")
        bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Welcome to BRANDOFA! Press Start to begin.")
