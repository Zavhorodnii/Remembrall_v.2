import Buttons
import CheckUserData
import TelegramCalendar

date = None
time = None


def create_date_select(update):
    update.message.reply_text(
        "Когда должно быть выведено напоминание?\nВыбрать можно на сегодня или позже.",
        reply_markup=Buttons.buttons_to_create_date_remem()
    )


def start_create(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text="Введите заголовок напоминания",
        reply_markup=Buttons.remove_button()
    )


def create_subscribe(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text="Введите текст напоминания"
    )


def create_date(update, context):
    context.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text="Введите дату в формате \'ДД.ММ.ГГ\'"
    )


def create_date_today(update, context, database):
    dates = CheckUserData.create_today()
    send_date(update.callback_query.message.chat_id, database, dates)
    dates = str(dates).split('-')
    dates = '{}.{}.{}'.format(dates[2], dates[1], dates[0])
    global date
    date = dates
    context.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text='Выбрано дату: ' + dates
    )


def create_date_calendar(update, context):
    context.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text=u"Выберите дату",
        reply_markup=Buttons.calendar()
    )


def change_calendar(update, context, datebase):
    try:
        selected, date_ = TelegramCalendar.process_calendar_selection(context.bot, update)
        if selected:
            global date
            date = CheckUserData.check_calendar_date(date_)
        context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Выбрана дата %s" % (date_.strftime("%d.%m.%Y"))
        )
        date_ = str(date_).split(' ')
        send_date(update.callback_query.message.chat_id, datebase, date_[0])
        return True
    except Exception as exe:
        return False


def create_time(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text="Ведите время в формате \'ЧЧ:ММ\'"
    )


def check_user_date(update, context, database):
    result = CheckUserData.check_date(update.message.text)
    if result[0] == 0:
        global date
        date = result[1]
        dates = result[1].split('.')
        dates = '{}-{}-{}'.format(dates[2], dates[1], dates[0])
        send_date(update.message.from_user.id, database, dates)
        return True
    else:
        send_mess(update, context, result[1])
        return False


def check_user_time(update, context, database):
    result = CheckUserData.check_time(update.message.text)
    if result[0] == 0:
        global date
        if date is None:
            date = database.last_date_remember(update.message.from_user.id)
            dates = date.split('-')
            date = '{}.{}.{}'.format(dates[2], dates[1], dates[0])
        global time
        time = result[1]
        times = '{}:00'.format(result[1])
        send_time(update.message.from_user.id, database, times)
        return True
    else:
        send_mess(update, context, result[1])
        return False


def send_mess(update, context, mess):
    context.bot.send_message(
        update.effective_chat.id,
        text=mess
    )


def send_title(update, database):
    database.send_title(update.message.from_user.id, update.message.text)


def send_subscribe(update, database):
    database.send_subscribe(update.message.from_user.id, update.message.text)


def send_date(user_id, database, dates):
    database.send_date(user_id, dates)


def send_time(user_id, database, times):
    database.send_time(user_id, times)


def successful_create_rem(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text="Напоминание появится {} в {}".format(date, time),
        reply_markup=Buttons.main_button()
    )
