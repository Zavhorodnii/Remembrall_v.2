import Buttons


class CommandStart:
    def __init__(self, database, buttons):
        self.__database = database
        self.__buttons = buttons

    def start(self, update, context):
        context.bot.send_message(
            update.effective_chat.id,
            text="Чтобы создать напоминание следуйте инструкциям и используйте"
                 " функциональные кнопки под строкой ввода",
            reply_markup=self.__buttons.main_button()
        )