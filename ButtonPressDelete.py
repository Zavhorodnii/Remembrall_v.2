from threading import Thread


class ButtonPressDelete:
    def __init__(self, database, threads):
        self.__database = database
        self.__threads = threads

    def delete_reminder(self, update, context):
        try:
            var = self.__database.select_repeat_message(update.callback_query.message.chat_id, update.callback_query.message.message_id)
            self.__threads.del_reminder_from_dict_reminder(self.__database.elect_one_reminder_before_delete(
                update.callback_query.message.chat_id, update.callback_query.message.message_id))
            self.__database.delete_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
            thread = Thread(target=self.delete, args=(update, context, var))
            thread.start()
        except Exception as exe:
            pass


    def delete(self, update, context, var):
        for delete_ in var:
            try:
                context.bot.edit_message_text(
                    chat_id=update.callback_query.message.chat_id,
                    message_id=delete_[0],
                    text='Сообщение удалено'
                )
            except Exception as exe:
                pass
