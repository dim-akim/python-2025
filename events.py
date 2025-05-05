import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          CallbackQueryHandler,
                          ConversationHandler,
                          filters)

from services import get_worker_list


log = logging.getLogger(__name__)
WAIT_FOR_DATE, WAIT_FOR_PLACE, WAIT_FOR_WORKER = range(3)


async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'ask_date is triggered by {update.effective_user}')
    text = 'Когда будет мероприятие?'
    await update.message.reply_text(text)

    return WAIT_FOR_DATE


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'get_date is triggered by {update.effective_user}')
    day = update.message.text
    context.user_data["day"] = day
    text = f'Я понял, мероприятие в эту дату: {day}'
    await update.message.reply_text(text)

    return await ask_place(update, context)


async def ask_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'ask_place is triggered by {update.effective_user}')
    buttons = [
        [InlineKeyboardButton('Зал', callback_data='Зал'),
         InlineKeyboardButton('Двор', callback_data='Двор')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Где именно будет проходить мероприятие?',
        reply_markup=keyboard
    )

    return WAIT_FOR_PLACE


async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'get_place is triggered by {update.effective_user}')
    query = update.callback_query
    context.user_data["place"] = query.data
    await query.answer('Зафиксировали')

    return await ask_worker(update, context)


async def ask_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'ask_worker is triggered by {update.effective_user}')
    workers = get_worker_list()
    buttons = [[InlineKeyboardButton(text="Любой", callback_data="Любой")]]
    for worker in workers:
        buttons.append([InlineKeyboardButton(text=worker, callback_data=worker)])
    keyboard = InlineKeyboardMarkup(buttons)

    query = update.callback_query
    await query.edit_message_text(
        text='Нужен ли кто-то конкретный из группы Актового зала?',
        reply_markup=keyboard
    )
    return WAIT_FOR_WORKER


async def get_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'get_worker is triggered by {update.effective_user}')
    query = update.callback_query
    await query.answer('Принято')

    return await register_application(update, context)


async def register_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'register_application is triggered by {update.effective_user}')
    day = context.user_data["day"]
    place = context.user_data["place"]
    worker = update.callback_query.data
    text = ['Заявка зарегистрирована:',
            f'Дата: {day}',
            f'Работник: {worker}',
            f'Место: {place}']
    text = '\n'.join(text)
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text
    )
    context.user_data.clear()
    return ConversationHandler.END


events_application_handler = ConversationHandler(
    entry_points=[CommandHandler('events', ask_date)],
    states={
        WAIT_FOR_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
        WAIT_FOR_PLACE: [CallbackQueryHandler(get_place)],
        WAIT_FOR_WORKER: [CallbackQueryHandler(get_worker)],
    },
    fallbacks=[]
)
