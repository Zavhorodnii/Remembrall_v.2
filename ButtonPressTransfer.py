from threading import Thread



class ButtonPressTransfer:
    def __init__(self, database, threads, buttons):

        self.__database = database
        self.__threads = threads
        self.__buttons = buttons
        self.__update_reminder = None


    def transfer_reminder(self, update, context):
        editing = 0
        if self.__update_reminder is None:
            editing = self.__database.check_editing_reminder(update.callback_query.message.chat_id)
        if editing != 0:
            return
        self.__update_reminder = False
        var = self.__database.select_one_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)
        self.__database.start_editing_reminder(update.callback_query.message.chat_id, update.callback_query.message.message_id)

        correct_date = str(var[3]).split('-')

        call_reminder = context.bot.send_message(
            update.effective_chat.id,
            text="{}\n{}\nДата {}.{}.{}nВремя {}".format(var[1], var[2], correct_date[2], correct_date[1],
                                                         correct_date[0], var[4]),
            reply_markup=self.__buttons.transfer_remind()
        )
        self.__database.add_id_reminder(update.effective_chat.id, call_reminder.message_id, var[0])


    def cancel_update_date(self, update, context):
        try:
            if self.__database.check_editing_reminder(update.callback_query.message.chat_id) == 0:
                return
            var = self.__database.select_one_reminder_where_editing_equal_true(update.callback_query.message.chat_id)
            last_reminder = update.callback_query.message.message_id
        except Exception as ex:
            if self.__database.check_editing_reminder(update.effective_chat.id) == 0:
                return
            var = self.__database.select_one_reminder_where_editing_equal_true(update.effective_chat.id)
            last_reminder = self.__database.select_last_repeat_message_with_id_reminder(update.effective_chat.id, var[0])[0]
        correct_date = str(var[4]).split('-')
        context.bot.edit_message_text(
            chat_id=var[1],
            message_id=last_reminder,
            text="{}\n{}\nДата {}.{}.{}\nВремя {}".format(var[2], var[3], correct_date[2], correct_date[1],
                                                          correct_date[0], var[5]),
            reply_markup=self.__buttons.button_control_mess()
        )
        self.__update_reminder = True
        self.finish_editing(var[1], 'cancel')


    def update_reminder_message(self, update, context,user_id):
        message = self.__database.select_one_reminder_where_editing_equal_true(user_id)
        all_repeat = self.__database.select_repeat_message_with_id_remember(user_id, message[0])
        thread = Thread(target=self.reminder, args=(context, user_id, message, all_repeat))
        thread.start()
        self.finish_editing(user_id, 'update')


    def reminder(self, context, user_id, message, all_repeat):
        for update_rem in all_repeat:
            correct_date = str(message[4]).split('-')
            try:
                context.bot.edit_message_text(
                    chat_id=user_id,
                    message_id=update_rem[0],
                    text="{}\n{}\nДата {}.{}.{}\nВремя {}".format(message[2], message[3], correct_date[2], correct_date[1],
                                                                  correct_date[0], message[5]),
                    reply_markup=self.__buttons.button_control_mess()
                )
            except Exception as exe:
                pass


    def finish_editing(self, user_id, str):
        if str == 'update':
            self.__threads.add_datetime_for_dict_remind(user_id)

        self.__database.finish_editing_reminder(user_id)