import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
import random
import sqlite3

conn = sqlite3.connect("./kamen_bd.sqlite3")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY, username TEXT,wins INT,lose INT)"
)
conn.commit()
conn.close()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["камень", "ножницы", "бумага"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    conn = sqlite3.connect("./kamen_bd.sqlite3")
    cursor = conn.cursor()
    select = cursor.execute(
        f"SELECT id from users where id = {update.effective_user.id}"
    )
    data = select.fetchone()
    if data == None:
        cursor.execute(
            f'INSERT INTO users VALUES({update.effective_user.id}, "{update.effective_user.username}",0,0)'
        )
        conn.commit()
    conn.close()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="привет это бот камень ножницы бумага",
        reply_markup=markup,
    )


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    a = random.randint(1, 3)
    result = 0
    player_choise = update.effective_message.text
    dic = {1: "камень", 2: "ножницы", 3: "бумага"}
    comp_choise = dic[a]
    text = comp_choise + "\n"
    if comp_choise == player_choise:
        text = text + "ничья🤨"
    if comp_choise == "камень" and player_choise == "бумага":
        text = text + "победа🥳"
        result = 1
    if comp_choise == "камень" and player_choise == "ножницы":
        text += "проигрыш😔"
        result = 2
    if comp_choise == "ножницы" and player_choise == "камень":
        text += "победа🥳"
        result = 1
    if comp_choise == "ножницы" and player_choise == "бумага":
        text += "проигрыш😔"
        result = 2
    if comp_choise == "бумага" and player_choise == "ножницы":
        text += "победа🥳"
        result = 1
    if comp_choise == "бумага" and player_choise == "камень":
        text += "проигрыш😔"
        result = 2
    conn = sqlite3.connect("./kamen_bd.sqlite3")
    cursor = conn.cursor()
    select = cursor.execute(
        f"SELECT id , wins , lose FROM users where  id = {update.effective_user.id}"
    )

    data = select.fetchone()
    if result == 1:
        cursor.execute(
            f"UPDATE users SET wins={data[1]+1} WHERE id = {update.effective_user.id}"
        )
    elif result == 2:
        cursor.execute(
            f"UPDATE users SET lose={data[2]+1} WHERE id = {update.effective_user.id}"
        )
    conn.commit()
    print(data)
    conn.close()
    keyboard = [
        [InlineKeyboardButton("статистика", callback_data="statistic")],
        [InlineKeyboardButton("повторить", callback_data="repiet")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=markup,
    )


async def callback_proc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # в этой фунции апдейт от результата игры
    # достаешь запрос из update
    query = update.callback_query
    # на любой callback нужно давать ответ
    await query.answer()

    data = query.data  # получаем данные из кнопки
    # это нужно чтобы
    if data == "statistic":
        conn = sqlite3.connect("./kamen_bd.sqlite3")
        cursor = conn.cursor()
        reselt = cursor.execute(
            f"SELECT id,wins,lose FROM users WHERE id={update.effective_user.id}"
        ).fetchone()
        text = f"ваша стаистика:победы-{reselt[1]}\n,проигрыши-{reselt[2]}"
        conn.close()
        keyboard = [[InlineKeyboardButton("повторить", callback_data="repiet")]]
        markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=text,
            reply_markup=markup,
        )
    elif data == "repiet":
        await start(update, context)


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
    # return должна вернуть строку 'Ваша статистика:/nПо'


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token("7037936272:AAEtrQ2z5qcCFi3OgP4Oj9LrdhWsqkPMVXk")
        .build()
    )
    print()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(
        MessageHandler(filters.Regex("^(камень|ножницы|бумага)$"), callback=game)
    )
    application.add_handler(CallbackQueryHandler(callback=callback_proc))
    application.run_polling()
