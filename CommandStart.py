import Buttons



def start(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text="Чтобы создато напоминание следуйте инструкциям и используйте"
             " функциональные кнопки под строкой ввода",
        reply_markup=Buttons.main_button()
    )