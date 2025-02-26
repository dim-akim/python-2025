from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config import TOKEN


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """функция, которая будет реагировать на команду /hello"""
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """функция, которая реагирует эхом на любое сообщение"""
    await update.message.reply_text(f'{update.message.text}')


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))  # регистрация обработчика
app.add_handler(MessageHandler(filters.ALL, echo))

print(f'Бот запущен')
app.run_polling()
print(f'Завершаем работу')
