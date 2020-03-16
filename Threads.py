from threading import Thread

import Buttons

dict_reminder = dict()


def start_thread(update, context, database):
    thread = Thread(target=create_thread, args=(update, context, database))
    thread.start()


def create_thread(update, context, database):

    while True:
        context.bot.send_message(
            update.effective_chat.id,
            text="threat",
            reply_markup=Buttons.button_control_mess()
        )