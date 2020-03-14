import logging

import DataBase
import ButtonPressCreate
import CommandStart
import RemembrallSettings
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import time

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

TELEGRAM_HTTP_API_TOKEN = '942544876:AAE4GMGwrVxMPF6qftwXhn6dEfBiLvicAdY'

CHOOSING, TITLE, SUBSCRIBE, DATE, TIME = range(5)


class Remembrall:
    def __init__(self):
        self.__remembrall = None
        self.__database = DataBase.DataBase()

    def start(self, update, context):
        CommandStart.start(update, context)
        return CHOOSING

    def create_title(self, update, context):
        ButtonPressCreate.start_create(update, context)
        return TITLE

    def check_title(self, update, context):
        ButtonPressCreate.send_title(update, self.__database)
        return self.create_subscribe(update, context)


    def create_subscribe(self, update, context):
        ButtonPressCreate.create_subscribe(update, context)
        return SUBSCRIBE

    def check_subscribe(self, update, context):
        ButtonPressCreate.send_subscribe(update, self.__database)
        return self.create_date(update, context)

    def create_date(self, update, context):
        ButtonPressCreate.create_date_select(update, context)
        return DATE

    def create_date_enter_by_hand(self, update, context):
        ButtonPressCreate.create_date(update, context)
        return DATE

    def create_date_today(self, update, context):
        ButtonPressCreate.create_date_today(update, context, self.__database)
        return self.create_time(update, context)

    def create_date_calendar(self, update, context):
        ButtonPressCreate.create_date_calendar(update, context)
        return DATE

    def change_calendar(self, update, context):
        if not ButtonPressCreate.change_calendar(update, context):
            return DATE
        else:
            return self.create_time(update, context)

    def check_date(self, update, context):
        if not ButtonPressCreate.check_user_date(update, context, self.__database):
            self.create_date(update, context)
        else:
            return self.create_time(update, context)


    def create_time(self, update, context):
        ButtonPressCreate.create_time(update, context)
        return TIME

    def check_time(self, update, context):
        if not ButtonPressCreate.check_user_time(update, context, self.__database):
            self.create_time(update, context)
        else:
            ButtonPressCreate.successful_create_rem(update, context)
            return CHOOSING

    def main(self, remembrall):
        self.__remembrall = remembrall
        updater = Updater(TELEGRAM_HTTP_API_TOKEN, use_context=True)
        dispatcher = updater.dispatcher


        control_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start),],
            states={
                CHOOSING: [
                    MessageHandler(Filters.regex('^Создать напоминание$'), self.create_title),
                ],
                TITLE: [
                    MessageHandler(Filters.text, self.check_title),
                ],
                SUBSCRIBE: [
                    MessageHandler(Filters.text, self.check_subscribe),
                ],
                DATE: [
                    CallbackQueryHandler(self.create_date_enter_by_hand, pass_user_data=True, pattern='{}$'.format('ENTER')),
                    CallbackQueryHandler(self.create_date_today, pass_user_data=True, pattern='{}$'.format('TODAY')),
                    CallbackQueryHandler(self.create_date_calendar, pass_user_data=True, pattern='{}$'.format('SELECT')),
                    CallbackQueryHandler(self.change_calendar),
                    MessageHandler(Filters.text, self.check_date)
                ],
                TIME: [
                    MessageHandler(Filters.text, self.check_time)
                ],
            },
            fallbacks=[],
        )
        dispatcher.add_handler(control_handler)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    # RemembrallSettings.first_settings_for_start_server()
    remembrall = Remembrall()
    remembrall.main(remembrall)