from flask import Flask, request
import telebot
from telebot import types

TOKEN = '8667764478:AAE4b8YF8B5cMmh86RzKWPAXmq6yPQAUDBE'
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- منطق البوت (نفس الذي كتبناه سابقاً مع تعديل بسيط) ---

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("تصميم جرافيك 🎨", "إنتاج فيديو 🎬")
    bot.send_message(message.chat.id, "أهلاً بك في برندوفا BRANDOFA 🚀\nاختر القسم المطلوب:", reply_markup=markup)

# إضافة بقية الـ handlers هنا (لوغو، بوست، إلخ) كما في الكود السابق...

# --- إعدادات Webhook الخاصة بـ Vercel ---

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Invalid Request', 403

@app.route('/')
def index():
    return "Bot is running..."