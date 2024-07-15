import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import sqlite3

conn = sqlite3.connect("./bd.sqlite3")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY, username TEXT,money INT)")
conn.commit()
conn.close()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('./bd.sqlite3')
    cursor = conn.cursor()
    select=cursor.execute(f'SELECT id from users where id = {update.effective_user.id}')
    data=select.fetchone()
    print(data)
    if data==None:
        cursor.execute(f'INSERT INTO users VALUES({update.effective_user.id}, "{update.effective_user.username}",0)')
        conn.commit()
    conn.close()
    await context.bot.send_message(

        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token("5859641374:AAHLX2rnOqLgqX72sGDqD_MAG6s4APnCviU")
        .build()
    )

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
