import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

from config import TOKEN
from events import events_application_handler


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(module)-15s [%(lineno)4d] - %(message)s'
)
logging.getLogger('httpx').setLevel(logging.WARNING)
log = logging.getLogger(__name__)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """функция, которая будет реагировать на команду /hello"""
    user = update.effective_user
    log.info(f'Функция hello вызвана пользователем {user}')
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """функция, которая реагирует эхом на любое сообщение"""
    user = update.effective_user
    message = update.message
    log.info(f'Функция echo вызвана пользователем {user}\n' + ' ' * 73 + f'{message = }')
    await update.message.reply_text(f'{update.message.text}')


async def say_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Рассказывает, какие есть возможности у бота"""
    user = update.effective_user
    log.info(f'Функция help вызвана пользователем {user}\n')

    text = [
        f'Привет, {user.first_name}!',
        '',
        'Я - школьный бот, который умеет реагировать на следующие команды:',
        '/hello - отвечаю приветствием',
        '/start /help - покажу список доступных команд',
        '/keyboard - покажу клавиатуру',
    ]
    text = '\n'.join(text)

    await update.message.reply_text(text)


async def say_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает inline-клавиатуру"""
    user = update.effective_user
    log.info(f'Функция say_keyboard вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('Раз', callback_data='Раз'),
         InlineKeyboardButton('Два', callback_data='Два'),
         InlineKeyboardButton('Три', callback_data='Три')],
        [InlineKeyboardButton('Четыре', callback_data='Четыре'),
         InlineKeyboardButton('Пять', callback_data='Пять')],
        [InlineKeyboardButton('Шесть', callback_data='Шесть')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Выберите опцию на клавиатуре',
        reply_markup=keyboard
    )


async def react_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Реагирует на нажатие кнопки на inline-клавиатуре"""
    user = update.effective_user
    log.info(f'Функция react_keyboard вызвана пользователем {user}')

    query = update.callback_query

    buttons = [
        [InlineKeyboardButton('Раз', callback_data='Раз'),
         InlineKeyboardButton('Два', callback_data='Два'),
         InlineKeyboardButton('Три', callback_data='Три')],
        [InlineKeyboardButton('Четыре', callback_data='Четыре'),
         InlineKeyboardButton('Пять', callback_data='Пять')],
        [InlineKeyboardButton('Шесть', callback_data='Шесть')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text=query.data,
        reply_markup=keyboard
    )


app = ApplicationBuilder().token(TOKEN).build()

# регистрация обработчиков
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler(["help", "start"], say_help))
app.add_handler(CommandHandler("keyboard", say_keyboard))
app.add_handler(CallbackQueryHandler(react_keyboard))
app.add_handler(events_application_handler)
app.add_handler(MessageHandler(filters.ALL, echo))

app.run_polling()
