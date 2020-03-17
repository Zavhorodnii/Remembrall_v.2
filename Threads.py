from datetime import datetime
from threading import Thread
from time import sleep

import Buttons
import DataBase

dict_reminder = dict()
updater = None


def add_datetime_for_dict_remind_after_restart(database, updater_):
    global dict_reminder, updater
    updater = updater_
    all_reminder = database.select_all_reminder_where_step_create_equal_zero()
    for i in all_reminder:
        dict_reminder[i[0]] = (i[1], "{} {}".format(i[4], i[5]))
        start_thread(i[0], i[1], i[2], i[3], database)
        sleep(0.1)
    print('dict_reminder ', dict_reminder)


def del_reminder_from_dict_reminder(message_id):
    global dict_reminder
    del dict_reminder[message_id[0]]


def add_datetime_for_dict_remind(database, user_id):
    global dict_reminder
    message = database.select_one_reminder_where_editing_equal_true(user_id)
    if message is None: #create
        message = database.select_last_remember(user_id)
        dict_reminder[message[0]] = (user_id, "{} {}".format(message[3], message[4]))
        start_thread(message[0], user_id, message[1], message[2], database)
    else:
        dict_reminder[message[0]] = (user_id, "{} {}".format(message[4], message[5]))


def start_thread(message_id, user_id, title, subscribe, database):
    thread = Thread(target=create_thread, args=(message_id, user_id, title, subscribe, database))
    thread.start()


def create_thread(message_id, user_id, title, subscribe, database):
    global updater, dict_reminder
    while True:
        if message_id not in dict_reminder:
            break
        time = database.allow_transfer_reminder(user_id)
        if time[0] != 0:
            sleep(15)
            continue
        date = datetime.strptime(dict_reminder[message_id][1], "%Y-%m-%d %H:%M:%S")
        if date <= datetime.now():
            date = dict_reminder[message_id][1].split(' ')
            correct_date = str(date[0]).split('-')
            call_reminder = updater.bot.send_message(
                user_id,
                text="{}\n{}\nДата {}.{}.{}\nВремя {}".format(title, subscribe, correct_date[2], correct_date[1],
                                                              correct_date[0], date[1]),
                reply_markup=Buttons.button_control_mess()
            )
            database.add_id_reminder(user_id, call_reminder.message_id, message_id)
            sleep(300)
        else:
            sleep(30)