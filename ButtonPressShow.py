from time import sleep

import Buttons


def show_remembral(update, context, database):
    all_remember = database.select_all_remember(update.message.from_user.id)
    print(len(all_remember))
    for remember in all_remember:
        try:
            call_reminder = context.bot.send_message(
                update.effective_chat.id,
                text="{}\n{}\n{}\nДата {}\nВремя {}".format(remember[0], remember[1], remember[2], remember[3], remember[4]),
                reply_markup=Buttons.button_control_mess()
            )
            database.add_id_reminder(call_reminder.message_id, remember[0])
        except Exception as exe:
            sleep(5)