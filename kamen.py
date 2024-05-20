import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import random
"""
сделать топ людей по победам
"""
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["камень", "ножницы", "бумага"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!",
        reply_markup=markup,
    )
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    a=random.randint(1,3)
    player_choise=update.effective_message.text
    dic={1:"камень",2:"ножницы",3:"бумага"}
    comp_choise=dic[a]
    text=comp_choise+"\n"
    if comp_choise == player_choise:
        text=text+"ничья🤨"
    if comp_choise == "камень" and player_choise == "бумага":
        text=text+"победа🥳"
    if comp_choise == "камень" and player_choise == "ножницы":
        text+="проигрыш😔"
    if comp_choise == "ножницы" and player_choise == "камень":
        text+="победа🥳"
    if comp_choise =="ножницы" and player_choise == "бумага":
        text+="проигрыш😔"
    if comp_choise == "бумага" and player_choise == "ножницы":
        text+="победа🥳"
    if comp_choise == "бумага"  and player_choise == "камень":
        text+="проигрыш😔"
    keyboard = [["камень", "ножницы", "бумага"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=markup,
    )
if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token("7037936272:AAEtrQ2z5qcCFi3OgP4Oj9LrdhWsqkPMVXk")
        .build()
    )

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.Regex("^(камень|ножницы|бумага)$"),callback=game))
    application.run_polling()
