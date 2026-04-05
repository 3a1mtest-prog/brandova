import telebot
from telebot import types

# الإعدادات الخاصة بك
TOKEN = '8667764478:AAE4b8YF8B5cMmh86RzKWPAXmq6yPQAUDBE'
ADMIN_ID = '8667764478'  # الآيدي الخاص بك لاستلام الإشعارات
bot = telebot.TeleBot(TOKEN)

# قاموس لتخزين حالة كل مستخدم (اللغة، الخدمة، التفاصيل)
user_states = {}

# الأسعار (بناءً على طلبك)
PRICES = {
    "بوست": "7 - 15$",
    "لوغو": "10 - 15$",
    "بانر": "10 - 15$",
    "ستوري": "5 - 7$",
    "موشن جرافيك": "100 - 150$ للدقيقة",
    "مونتاج عادي": "30 - 50$ للدقيقة"
}

# 1. رسالة البداية واختيار اللغة
@bot.message_handler(commands=['start'])
def start_cmd(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("العربية 🇸🇦", "English 🇺🇸")
    
    welcome_text = "مرحباً بك في شركة برندوفا BRANDOFA 🚀\nيرجى اختيار اللغة للبدء:\n\nWelcome to BRANDOFA! Please choose your language:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# 2. معالجة اختيار اللغة والترحيب
@bot.message_handler(func=lambda m: m.text in ["العربية 🇸🇦", "English 🇺🇸"])
def set_language(message):
    lang = "ar" if "العربية" in message.text else "en"
    user_states[message.chat.id] = {"lang": lang}
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "ar":
        msg = "أهلاً بك في برندوفا! نحن نصنع الإبداع. اختر ماذا تريد اليوم:"
        markup.add("تصميم صور 🎨", "إنتاج فيديو 🎬")
    else:
        msg = "Welcome to BRANDOFA! We create brilliance. Choose your service:"
        markup.add("Graphic Design 🎨", "Video Production 🎬")
    
    bot.send_message(message.chat.id, msg, reply_markup=markup)

# 3. معالجة التصنيفات الرئيسية (فيديو أو صور)
@bot.message_handler(func=lambda m: m.text in ["تصميم صور 🎨", "Graphic Design 🎨", "إنتاج فيديو 🎬", "Video Production 🎬"])
def main_service(message):
    chat_id = message.chat.id
    lang = user_states[chat_id]["lang"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if "صور" in message.text or "Design" in message.text:
        user_states[chat_id]["category"] = "Images"
        if lang == "ar":
            markup.add("لوغو", "بوست", "بانر", "ستوري", "رجوع ⬅️")
            msg = "اختر نوع التصميم المطلوب:"
        else:
            markup.add("Logo", "Post", "Banner", "Story", "Back ⬅️")
            msg = "Choose design type:"
            
    else:
        user_states[chat_id]["category"] = "Video"
        if lang == "ar":
            markup.add("موشن جرافيك", "مونتاج عادي", "رجوع ⬅️")
            msg = "اختر نوع الفيديو المطلوب:"
        else:
            markup.add("Motion Graphics", "Standard Editing", "Back ⬅️")
            msg = "Choose video type:"
            
    bot.send_message(chat_id, msg, reply_markup=markup)

# 4. معالجة التفريعات النهائية (الخدمة المحددة) والأسعار
@bot.message_handler(func=lambda m: m.text in ["لوغو", "Logo", "بوست", "Post", "بانر", "Banner", "ستوري", "Story", "موشن جرافيك", "Motion Graphics", "مونتاج عادي", "Standard Editing"])
def sub_service(message):
    chat_id = message.chat.id
    lang = user_states[chat_id]["lang"]
    service_name = message.text
    
    # تحويل الاسم للعربي للبحث في قاموس الأسعار
    translate_map = {
        "Logo": "لوغو", "Post": "بوست", "Banner": "بانر", "Story": "ستوري",
        "Motion Graphics": "موشن جرافيك", "Standard Editing": "مونتاج عادي"
    }
    key = translate_map.get(service_name, service_name)
    price = PRICES.get(key, "حسب الاتفاق")
    
    if lang == "ar":
        response = f"✅ اختيارك: {service_name}\n💰 التسعيرة التقريبية: {price}\n\nشكراً لثقتك بـ **برندوفا**. سيتواصل معك فريقنا الآن لتأكيد الطلب."
    else:
        response = f"✅ Your Choice: {service_name}\n💰 Estimated Price: {price}\n\nThank you for choosing **BRANDOFA**. Our team will contact you shortly."
    
    bot.send_message(chat_id, response)
    
    # 5. إرسال الإشعار للمدير (أنت)
    admin_notify = (
        f"🔔 **طلب جديد لشركة برندوفا**\n\n"
        f"👤 العميل: {message.from_user.first_name}\n"
        f"🔗 اليوزر: @{message.from_user.username}\n"
        f"🛠 الخدمة: {service_name}\n"
        f"💵 التسعيرة المعطاة: {price}"
    )
    bot.send_message(ADMIN_ID, admin_notify)

# معالجة زر الرجوع
@bot.message_handler(func=lambda m: "رجوع" in m.text or "Back" in m.text)
def back_button(message):
    set_language(message)

bot.polling(none_stop=True)
