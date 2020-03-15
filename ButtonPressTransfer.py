from threading import Thread

import Buttons

update_reminder = None


def transfer_reminder(update, context, database):
    print("++")
    editing = 0
    global update_reminder
    if update_reminder is None:
        print('update_reminder')
        editing = database.check_editing_reminder(update.callback_query.message.chat_id)
    print('editing ', editing)
    if editing != 0:
        return
    update_reminder = False
    var = database.select_one_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
    database.start_editing_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
    print("var ", var)
    call_reminder = context.bot.send_message(
        update.effective_chat.id,
        text="{}\n{}\n{}\nДата {}\nВремя {}".format(var[0], var[1], var[2], var[3], var[4]),
        reply_markup=Buttons.transfer_remind()
    )
    database.add_id_reminder(update.effective_chat.id, call_reminder.message_id, var[0])


def cancel_update_date(update, context, database):
    print('cancel')
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
