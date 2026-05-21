import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# Логларни созлаш
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Бот Токени
BOT_TOKEN = "7737227749:AAFXpWbE2O5VstqD2GjCH1iC59bRE7g0rRE"

# Рўйхатдан ўтиш босқичлари
LANGUAGE, NAME, PHONE, MAIN_MENU = range(4)

# Тил танлаш тугмалари
lang_keyboard = [
    [KeyboardButton("🇺🇿 O'zbekcha"), KeyboardButton("🇷🇺 Русский")]
]
lang_markup = ReplyKeyboardMarkup(lang_keyboard, resize_keyboard=True, one_time_keyboard=True)

# 1. СТАРТ БУЙРУҒИ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "Assalomu alaykum! Biotehnoeko botiga xush kelibsiz.\n"
        "Iltimos, tilni tanlang:\n\n"
        "Здравствуйте! Добро пожаловать в бот Биотехноэко.\n"
        "Пожалуйста, выберите язык:",
        reply_markup=lang_markup
    )
    return LANGUAGE

# 2. ТИЛ ТАНЛАШ
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "🇺🇿 O'zbekcha":
        context.user_data['lang'] = 'uz'
        await update.message.reply_text("Ismingizni kiriting:")
    elif text == "🇷🇺 Русский":
        context.user_data['lang'] = 'ru'
        await update.message.reply_text("Введите ваше имя:")
    else:
        await update.message.reply_text("Iltimos, tugmalardan birini tanlang / Пожалуйста, выберите одну из кнопок.")
        return LANGUAGE
    return NAME

# 3. ИСМНИ ҚАБУЛ ҚИЛИШ
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text
    context.user_data['name'] = name
    lang = context.user_data.get('lang', 'uz')
    
    if lang == 'uz':
        phone_keyboard = [[KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]]
        phone_markup = ReplyKeyboardMarkup(phone_keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(f"Rahmat, {name}! Endi telefon raqamingizni yuboring:", reply_markup=phone_markup)
    else:
        phone_keyboard = [[KeyboardButton("📞 Отправить номер телефона", request_contact=True)]]
        phone_markup = ReplyKeyboardMarkup(phone_keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(f"Спасибо, {name}! Теперь отправьте ваш номер телефона:", reply_markup=phone_markup)
    return PHONE

# 4. ТЕЛЕФОН РАҚАМНИ ҚАБУЛ ҚИЛИШ ВА МЕНЮГА ЎТИШ
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    contact = update.message.contact
    lang = context.user_data.get('lang', 'uz')
    
    if contact:
        phone = contact.phone_number
    else:
        phone = update.message.text
        
    context.user_data['phone'] = phone
    
    if lang == 'uz':
        main_keyboard = [["📝 Ariza qoldirish"], ["ℹ️ Ma'lumot", "⚙️ Sozlamalar"]]
        main_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
        await update.message.reply_text("Ro'yxatdan muvaffaqiyatli o'tdingiz! Asosiy menyu:", reply_markup=main_markup)
    else:
        main_keyboard = [["📝 Оставить заявку"], ["ℹ️ Информация", "⚙️ Настройки"]]
        main_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
        await update.message.reply_text("Вы успешно зарегистрировались! Главное меню:", reply_markup=main_markup)
    return MAIN_MENU

# БЕКОР ҚИЛИШ БУЙРУҒИ
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('lang', 'uz')
    context.user_data.clear()
    if lang == 'uz':
        await update.message.reply_text("Jarayon bekor qilindi. Qayta boshlash uchun /start bosing.")
    else:
        await update.message.reply_text("Процесс отменен. Для начала заново нажмите /start.")
    return ConversationHandler.END

# АСОСИЙ ИШГА ТУШИРИШ ФУНКЦИЯСИ
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_language)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)
            ],
            MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: MAIN_MENU) 
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    logger.info("Бот муваффақиятли ишга тушди...")
    application.run_polling()

if __name__ == '__main__':
    main()
