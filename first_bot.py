import logging
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
    
)

# логирование-сбор информации о работе бота
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# корутины
# :Update — это подсказка для VScode какие подсказки тебе давать
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_user.name)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.effective_user.first_name}, здесь не общаются голосовыми",
    )


async def creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Да, это мой создатель",
    )


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_user.name)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"привет , {update.effective_user.name}"
    )


"""
update — это словарь в котором лежит вся информация об 
пользователе сообщении чате и многое другое

context — информация о данных бота. user_data bot_data chat_data
"""

# запрет на запуск при импорте
if __name__ == "__main__":
    # обЪект класса приложения
    application = (
        ApplicationBuilder()
        .token("5859641374:AAHLX2rnOqLgqX72sGDqD_MAG6s4APnCviU")
        .build()
    )

    # handler-обработчик
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.VOICE, voice_message))
    application.add_handler(MessageHandler(filters.Regex("^привет$"), hello))
    application.add_handler(
        MessageHandler(filters.Regex("^(Леха|Алексей|Лехаридзе)$"), creator)
    )
    # запуск лонг полинг-долкий опрос
    application.run_polling()
