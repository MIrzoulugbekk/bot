from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# /start komandasi uchun handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Salom! Men oddiy Telegram botman. Xabar yozing, men uni qaytaraman!")

# Xabarlarni qaytaruvchi handler
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def main():
    TOKEN = "7577882781:AAHrG-Qxe_4-0pqs4s8G4LKAqnucj677uOI"  # O'zingizning bot tokeningizni kiriting
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Komanda va xabar handlerlarini qo'shish
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
