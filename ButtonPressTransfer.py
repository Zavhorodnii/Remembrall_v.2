from threading import Thread

import Buttons
import Threads

update_reminder = None


def transfer_reminder(update, context, database):
    editing = 0
    global update_reminder
    if update_reminder is None:
        editing = database.check_editing_reminder(update.callback_query.message.chat_id)
    if editing != 0:
        return
    update_reminder = False
    var = database.select_one_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
    database.start_editing_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)

    correct_date = str(var[3]).split('-')

    call_reminder = context.bot.send_message(
        update.effective_chat.id,
        text="{}\n{}\nДата {}.{}.{}nВремя {}".format(var[1], var[2], correct_date[2], correct_date[1],
                                                     correct_date[0], var[4]),
        reply_markup=Buttons.transfer_remind()
    )
    database.add_id_reminder(update.effective_chat.id, call_reminder.message_id, var[0])


def cancel_update_date(update, context, database):
    try:
        if database.check_editing_reminder(update.callback_query.message.chat_id) == 0:
            return
        var = database.select_one_reminder_where_editing_equal_true(update.callback_query.message.chat_id)
        last_reminder = update.callback_query.message.message_id
    except Exception as ex:
        if database.check_editing_reminder(update.effective_chat.id) == 0:
            return
        var = database.select_one_reminder_where_editing_equal_true(update.effective_chat.id)
        last_reminder = database.select_last_repeat_message_with_id_reminder(update.effective_chat.id, var[0])[0]
    correct_date = str(var[4]).split('-')
    context.bot.edit_message_text(
        chat_id=var[1],
        message_id=last_reminder,
        text="{}\n{}\nДата {}.{}.{}\nВремя {}".format(var[2], var[3], correct_date[2], correct_date[1],
                                                      correct_date[0], var[5]),
        reply_markup=Buttons.button_control_mess()
    )
    global update_reminder
    update_reminder = True
    finish_editing(database, var[1], 'cancel')


def update_reminder_message(update, context, database, user_id):
    message = database.select_one_reminder_where_editing_equal_true(user_id)
    all_repeat = database.select_repeat_message_with_id_remember(user_id, message[0])
    thread = Thread(target=reminder, args=(context, user_id, message, all_repeat))
    thread.start()
    finish_editing(database, user_id, 'update')


def reminder(context, user_id, message, all_repeat):
    for update_rem in all_repeat:
        correct_date = str(message[4]).split('-')
        try:
            context.bot.edit_message_text(
                chat_id=user_id,
                message_id=update_rem[0],
                text="{}\n{}\nДата {}.{}.{}\nВремя {}".format(message[2], message[3], correct_date[2], correct_date[1],
                                                              correct_date[0], message[5]),
                reply_markup=Buttons.button_control_mess()
            )
        except Exception as exe:
            pass


def finish_editing(database, user_id, str):
    if str == 'update':
        Threads.add_datetime_for_dict_remind(database, user_id)
    
    database.finish_editing_reminder(user_id)