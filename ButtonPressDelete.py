from threading import Thread

import Threads


def delete_reminder(update, context, database):
    print('delete_reminder')
    # print(update.callback_query.message.message_id)
    var = database.select_repeat_message(update.callback_query.message.chat_id, update.callback_query.message.message_id)
    Threads.del_reminder_from_dict_reminder(database.elect_one_reminder_before_delete(
        update.callback_query.message.chat_id, update.callback_query.message.message_id))
    database.delete_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
    thread = Thread(target=delete, args=(update, context, var))
    thread.start()


def delete(update, context, var):
    for delete_ in var:
        try:
            context.bot.edit_message_text(
                chat_id=update.callback_query.message.chat_id,
                message_id=delete_[0],
                text='Сообщение удалено'
            )
        except Exception as exe:
            pass
