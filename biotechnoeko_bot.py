#!/usr/bin/env python3
import os, logging, random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DISPATCHER = "@BioTexnoEkojamoa"                                                             
def gen_num():
    return random.randint(10000, 99999)

(LANG, MENU, COMP_ADDR, APP_TYPE, APP_NUM, APP_NAME, APP_INN, APP_SELECT, APP_CONFIRM, APP_DATE, APP_VOLUME) = range(11)

def lang_kb():
    return ReplyKeyboardMarkup([["O'zbek", "Русский", "English"]], resize_keyboard=True)

def menu_kb(lang):
    b = {"uz": [["Shikoyat", "Yuridik shaxs zayavkasi"]], "ru": [["Zhaloba", "Zayavka yur. litsa"]], "en": [["Complaint", "Legal Entity Application"]]}
    return ReplyKeyboardMarkup(b[lang], resize_keyboard=True)

def search_kb(lang):
    b = {"uz": [["Shartnoma raqami"], ["Korxona nomi"], ["INN raqami"], ["Orqaga"]], "ru": [["Nomer dogovora"], ["Nazvanie org"], ["INN"], ["Nazad"]], "en": [["Contract number"], ["Org name"], ["Tax ID"], ["Back"]]}
    return ReplyKeyboardMarkup(b[lang], resize_keyboard=True)

def yn_kb(lang):
    b = {"uz": [["Ha, zayavka beraman", "Yoq"]], "ru": [["Da, podat", "Net"]], "en": [["Yes, submit", "No"]]}
    return ReplyKeyboardMarkup(b[lang], resize_keyboard=True)
    async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text("Assalomu alaykum! BioTechnoEko\n\nTilni tanlang:", reply_markup=lang_kb())
    return LANG

async def set_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "zbek" in text: lang = "uz"
    elif "усский" in text: lang = "ru"
    else: lang = "en"
    ctx.user_data["lang"] = lang
    msgs = {"uz": "Xizmat turini tanlang:", "ru": "Viberite uslugu:", "en": "Select a service:"}
    await update.message.reply_text(msgs[lang], reply_markup=menu_kb(lang))
    return MENU

async def menu_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "uz")
    text = update.message.text
    if any(w in text for w in ["Shikoyat", "Zhaloba", "Complaint"]):
        msgs = {"uz": "Manzilingizni yuboring:", "ru": "Otpravte adres:", "en": "Send your address:"}
        await update.message.reply_text(msgs[lang], reply_markup=ReplyKeyboardRemove())
        return COMP_ADDR
    elif any(w in text for w in ["Yuridik", "Zayavka", "Legal"]):
        msgs = {"uz": "Shartnomani qanday topamiz?", "ru": "Kak najdem dogovor?", "en": "How to find contract?"}
        await update.message.reply_text(msgs[lang], reply_markup=search_kb(lang))
        return APP_TYPE
    await update.message.reply_text("...", reply_markup=menu_kb(lang))
    return MENU
    async def complaint_addr(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "uz")
    addr = update.message.text
    num = gen_num()
    u = update.message.from_user
    uname = u.username if u.username else "noma'lum"
    msg = f"YANGI SHIKOYAT #{num}\nFoydalanuvchi: {u.full_name} @{uname}\nManzil: {addr}\nTil: {lang.upper()}"
    try:
        await ctx.bot.send_message(chat_id=DISPATCHER, text=msg)
    except Exception as e:
        logger.error(f"Xato: {e}")
    msgs = {"uz": f"Shikoyat qabul qilindi! #{num}\nDispatcher: {DISPATCHER}", "ru": f"Zhaloba prinyata! #{num}\nDispetcher: {DISPATCHER}", "en": f"Complaint received! #{num}\nDispatcher: {DISPATCHER}"}
    await update.message.reply_text(msgs[lang], reply_markup=menu_kb(lang))
    return MENU

async def app_type(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "uz")
    text = update.message.text
    if any(w in text for w in ["Orqaga", "Nazad", "Back"]):
        await update.message.reply_text("...", reply_markup=menu_kb(lang))
        return MENU
    elif any(w in text for w in ["raqami", "Nomer", "number"]):
        msgs = {"uz": "Shartnoma raqamini yuboring:", "ru": "Otpravte nomer dogovora:", "en": "Send contract number:"}
        await update.message.reply_text(msgs[lang], reply_markup=ReplyKeyboardRemove())
        return APP_NUM
    elif any(w in text for w in ["nomi", "Nazvanie", "name"]):
        msgs = {"uz": "Korxona nomini yuboring:", "ru": "Otpravte nazvanie:", "en": "Send org name:"}
        await update.message.reply_text(msgs[lang], reply_markup=ReplyKeyboardRemove())
        return APP_NAME
    elif any(w in text for w in ["INN", "Tax"]):
        msgs = {"uz": "INN yuboring:", "ru": "Otpravte INN:", "en": "Send Tax ID:"}
        await update.message.reply_text(msgs[lang], reply_markup=ReplyKeyboardRemove())
        return APP_INN
    await update.message.reply_text("...", reply_markup=search_kb(lang))
    return APP_TYPE
    reply_text(msgs[lang], reply_markup=ReplyKeyboardRemove())
    return APP_VOLUME

async def app_volume(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "uz")
    volume = update.message.text
    date = ctx.user_data.get("date", "-")
    c = ctx.user_data.get("contract", {})
    num = gen_num()
    u = update.message.from_user
    uname = u.username if u.username else "noma'lum"
    msg = f"YANGI ZAYAVKA #{num}\nKorxona: {c.get('korxona','?')}\nShartnoma: {c.get('raqam','?')}\nSana: {date}\nHajm: {volume}\nFoydalanuvchi: {u.full_name} @{uname}"
    try:
        await ctx.bot.send_message(chat_id=DISPATCHER, text=msg)
    except Exception as e:
        logger.error(f"Xato: {e}")
    msgs = {"uz": f"Zayavka qabul qilindi! #{num}\nDispatcher: {DISPATCHER}", "ru": f"Zayavka prinyata! #{num}\n{DISPATCHER}", "en": f"Application accepted! #{num}\n{DISPATCHER}"}
    await update.message.reply_text(msgs[lang], reply_markup=menu_kb(lang))
    return MENU

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi. /start", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
            COMP_ADDR: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_addr)],
            APP_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, app_type)],
            APP_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, app_by_num)],
            APP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, app_by_name)],
            APP_INN: [MessageHandler(filters.TEXT & ~filters.COMMAND, app_by_inn)],
            APP_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, app_select)],
            APP_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, app_confirm)],
            APP_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, app_date)],
            APP_VOLUME: [MessageHandler(filters.TEXT & ~filters.COMMAND, app_volume)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
        allow_reentry=True,
    )
    app.add_handler(conv)
    print("Bot ishga tushdi!")
    app.run_polling()

if name == "__main__":
    main()
