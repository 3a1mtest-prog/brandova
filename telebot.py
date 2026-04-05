import telebot
from telebot import types

TOKEN = '8667764478:AAE4b8YF8B5cMmh86RzKWPAXmq6yPQAUDBE'
ADMIN_ID = '8667764478'  # الآيدي الخاص بك لاستلام الطلبات
bot = telebot.TeleBot(TOKEN)

# تخزين بيانات العميل مؤقتاً
user_data = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("تصميم جرافيك 🎨")
    item2 = types.KeyboardButton("إنتاج فيديو 🎬")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, f"أهلاً بك في **برندوفا BRANDOFA** 🚀\nنحن هنا لتحويل أفكارك إلى واقع. اختر القسم الذي يهمك:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_options(message):
    chat_id = message.chat.id
    
    if message.text == "تصميم جرافيك 🎨":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("لوغو", "بوست", "بانر", "ستوري", "رجوع")
        bot.send_message(chat_id, "اختر نوع التصميم المطللوب:", reply_markup=markup)
        
    elif message.text == "إنتاج فيديو 🎬":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("مونتاج عادي", "موشن جرافيك", "رجوع")
        bot.send_message(chat_id, "اختر نوع الفيديو:", reply_markup=markup)

    # تفريعات الأسعار
    elif message.text in ["لوغو", "بوست", "بانر", "ستوري"]:
        user_data[chat_id] = {'type': message.text}
        prices = {"لوغو": "10-15$", "بوست": "7-15$", "بانر": "10-15$", "ستوري": "5-7$"}
        bot.send_message(chat_id, f"سعر {message.text} يتراوح بين {prices[message.text]}.\nكم عدد التصاميم المطلوبة؟")
        bot.register_next_step_handler(message, process_quantity)

    elif message.text in ["مونتاج عادي", "موشن جرافيك"]:
        user_data[chat_id] = {'type': message.text}
        prices = {"مونتاج عادي": "30-50$", "موشن جرافيك": "100-150$"}
        bot.send_message(chat_id, f"سعر دقيقة {message.text} يتراوح بين {prices[message.text]}.\nكم دقيقة تحتاج؟")
        bot.register_next_step_handler(message, process_duration)
        
    elif message.text == "رجوع":
        welcome(message)

def process_quantity(message):
    chat_id = message.chat.id
    qty = message.text
    user_data[chat_id]['amount'] = qty
    send_summary(message)

def process_duration(message):
    chat_id = message.chat.id
    duration = message.text
    user_data[chat_id]['amount'] = duration
    send_summary(message)

def send_summary(message):
    chat_id = message.chat.id
    data = user_data.get(chat_id)
    
    summary = f"✅ تم استلام طلبك بنجاح!\nالخدمة: {data['type']}\nالكمية/المدة: {data['amount']}\nسيتواصل معك فريق **برندوفا** قريباً."
    bot.send_message(chat_id, summary)
    
    # إرسال إشعار لصاحب الشركة (أنت)
    admin_msg = f"🔔 **طلب جديد من عميل!**\nالعميل: @{message.from_user.username or message.from_user.first_name}\nالخدمة: {data['type']}\nالتفاصيل: {data['amount']}"
    bot.send_message(ADMIN_ID, admin_msg)

bot.polling()
