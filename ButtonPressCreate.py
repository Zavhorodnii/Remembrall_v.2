import Buttons
import CheckUserData

date = None
time = None


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
    context.bot.send_message(
        update.effective_chat.id,
        text="Введите дату в формате \'ДД.ММ.ГГ\'"
    )
    # context.bot.edit_message_text(
    #     chat_id=update.callback_query.message.chat_id,
    #     message_id=update.callback_query.message.message_id,
    #     text="Введите дату в формате \'ДД.ММ.ГГ\'"
    # )


def create_time(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text="Ведите время в формате \'ЧЧ:ММ\'"
    )


def check_user_date(update, context, database):
    result = CheckUserData.check_date(update.message.text)
    print(result)
    if result[0] == 0:
        global date
        date = result[1]
        send_date(update.message.from_user.id, database)
        return True
    else:
        error(update, context, result[1])
        return False


def check_user_time(update, context, database):
    result = CheckUserData.check_time(update.message.text)
    if result[0] == 0:
        global time
        time = result[1]
        send_time(update.message.from_user.id, database)
        return True
    else:
        error(update, context, result[1])
        return False


def error(update, context, mess):
    context.bot.send_message(
        update.effective_chat.id,
        text=mess
    )


def send_title(update, database):
    database.send_title(update.message.from_user.id, update.message.text)


def send_subscribe(update, database):
    database.send_subscribe(update.message.from_user.id, update.message.text)


def send_date(user_id, database):
    global date
    dates = date.split('.')
    date_ = '{}-{}-{}'.format(dates[2], dates[1], dates[0])
    print('date: ', date_)
    database.send_date(user_id, date_)


def send_time(user_id, database):
    times = '{}:00'.format(time)
    database.send_time(user_id, times)


def successful_create_rem(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text="Напоминание Появится {} в {}".format(date, time),
        reply_markup=Buttons.main_button()
    )
