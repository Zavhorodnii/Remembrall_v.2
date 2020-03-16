from time import sleep

import Buttons


def show_remembral(update, context, database):
    all_remember = database.select_all_remember(update.message.from_user.id)
    if len(all_remember) == 0:
        context.bot.send_message(
            update.effective_chat.id,
            text="У вас нету напоминаний",
        )
    for remember in all_remember:
        try:
            correct_date = str(remember[3]).split('-')
            call_reminder = context.bot.send_message(
                update.effective_chat.id,
                text="{}\n{}\nДата {}.{}.{}\nВремя {}".format(remember[1], remember[2], correct_date[2], correct_date[1],
                                                              correct_date[0], remember[4]),
                reply_markup=Buttons.button_control_mess()
            )
            database.add_id_reminder(update.effective_chat.id, call_reminder.message_id, remember[0])
        except Exception as exe:
            sleep(5)