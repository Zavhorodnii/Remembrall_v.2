from threading import Thread

import Buttons

update_reminder = None


def transfer_reminder(update, context, database):
    # print("++")
    editing = 0
    global update_reminder
    if update_reminder is None:
        # print('update_reminder')
        editing = database.check_editing_reminder(update.callback_query.message.chat_id)
    # print('editing ', editing)
    if editing != 0:
        return
    update_reminder = False
    var = database.select_one_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
    database.start_editing_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
    # print("var ", var)
    call_reminder = context.bot.send_message(
        update.effective_chat.id,
        text="{}\n{}\n{}\nДата {}\nВремя {}".format(var[0], var[1], var[2], var[3], var[4]),
        reply_markup=Buttons.transfer_remind()
    )
    database.add_id_reminder(update.effective_chat.id, call_reminder.message_id, var[0])


def cancel_update_date(update, context, database):
    database.finish_editing_reminder(update.callback_query.message.chat_id)
    var = database.select_one_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
    context.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text="{}\n{}\n{}\nДата {}\nВремя {}".format(var[0], var[1], var[2], var[3], var[4]),
        reply_markup=Buttons.button_control_mess()
    )
    global update_reminder
    update_reminder = True


def update_reminder_message(update, context, database, user_id):
    # print('update_reminder_message')
    message = database.select_one_reminder_where_editing_equal_true(user_id)
    # print('message ', message)
    all_repeat = database.select_repeat_message_with_id_remember(user_id, message[0])
    # print('all_repeat ', all_repeat)
    database.finish_editing_reminder(user_id)
    thread = Thread(target=reminder, args=(context, user_id, message, all_repeat))
    thread.start()


def reminder(context, user_id, message, all_repeat):
    for update_rem in all_repeat:
        try:
            context.bot.edit_message_text(
                chat_id=user_id,
                message_id=update_rem[0],
                text="{}\n{}\n{}\nДата {}\nВремя {}".format(message[0], message[1], message[2], message[3], message[4]),
                reply_markup=Buttons.button_control_mess()
            )
        except Exception as exe:
            pass