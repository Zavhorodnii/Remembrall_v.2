import logging

import ButtonPressDelete
import ButtonPressShow
import ButtonPressTransfer
import Buttons
import DataBase
import ButtonPressCreate
import CommandStart
import RemembrallSettings
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import Threads

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)


TELEGRAM_HTTP_API_TOKEN = '942544876:AAE4GMGwrVxMPF6qftwXhn6dEfBiLvicAdY'

CHOOSING, TITLE, SUBSCRIBE, DATE, CHECK_DATE, TIME = range(6)


class Remembrall:
    def __init__(self, database, remembral_settings):
        self.__buttons = Buttons.Buttons()
        self.__database = database
        self.__remembral_settings = remembral_settings
        self.__threads = Threads.Threads(self.__database, self.__buttons)
        self.__commandStart = CommandStart.CommandStart(self.__database, self.__buttons)
        self.__buttonPressShow = ButtonPressShow.ButtonPressShow(self.__database, self.__buttons)
        self.__buttonPressDelete = ButtonPressDelete.ButtonPressDelete(self.__database,  self.__threads)
        self.__buttonPressTransfer = ButtonPressTransfer.ButtonPressTransfer(self.__database, self.__threads, self.__buttons)
        self.__buttonPressCreate = ButtonPressCreate.ButtonPressCreate(self.__threads, self.__database, self.__buttons, self.__buttonPressTransfer)
        self.__remembrall = None

    def start(self, update, context):
        self.__buttonPressTransfer.cancel_update_date(update, context)
        self.__commandStart.start(update, context)
        return CHOOSING

    def create_title(self, update, context):
        self.__buttonPressTransfer.cancel_update_date(update, context)
        self.__buttonPressCreate.start_create(update, context)
        return TITLE

    def show_remembral(self, update, context):
        self.__buttonPressTransfer.cancel_update_date(update, context)
        self.__buttonPressShow.show_remembral(update, context)
        return CHOOSING

    def check_title(self, update, context):
        self.__buttonPressCreate.send_title(update)
        return self.create_subscribe(update, context)

    def create_subscribe(self, update, context):
        self.__buttonPressCreate.create_subscribe(update, context)
        return SUBSCRIBE

    def check_subscribe(self, update, context):
        self.__buttonPressCreate.send_subscribe(update)
        return self.create_date(update, context)

    def create_date(self, update, context):
        self.__buttonPressCreate.create_date_select(update)
        return DATE

    def create_date_enter_by_hand(self, update, context):
        self.__buttonPressCreate.create_date(update, context)
        return CHECK_DATE

    def create_date_today(self, update, context):
        self.__buttonPressCreate.create_date_today(update, context)
        return self.create_time(update, context)

    def create_date_calendar(self, update, context):
        self.__buttonPressCreate.create_date_calendar(update, context)
        return DATE

    def change_calendar(self, update, context):
        if not self.__buttonPressCreate.change_calendar(update, context):
            return DATE
        else:
            return self.create_time(update, context)

    def check_date(self, update, context):
        if not self.__buttonPressCreate.check_user_date(update, context):
            return self.create_date(update, context)
        else:
            return self.create_time(update, context)

    def create_time(self, update, context):
        self.__buttonPressCreate.create_time(update, context)
        return TIME

    def check_time(self, update, context):
        if not self.__buttonPressCreate.check_user_time(update, context):
            self.create_time(update, context)
        else:
            self.__buttonPressCreate.successful_create_rem(update, context)
            return CHOOSING

    def delete_reminder(self, update, context):
        self.__buttonPressDelete.delete_reminder(update, context)
        return CHOOSING

    def move_reminder(self, update, context):
        self.__buttonPressTransfer.transfer_reminder(update, context)
        return DATE

    def cancel_update_date(self, update, context):
        self.__buttonPressTransfer.cancel_update_date(update, context)
        return CHOOSING

    def start_after_restart(self, update, context):
        try:
            var = self.__remembral_settings.step_create(update)
            if var[0] == 3:
                return self.check_subscribe(update, context)
            elif var[0] == 1:
                return self.check_time(update, context)
        except Exception as exe:
            pass

    def main(self, remembrall):
        self.__remembrall = remembrall
        updater = Updater(TELEGRAM_HTTP_API_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        self.__threads.add_datetime_for_dict_remind_after_restart(updater)


        control_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start),
                          MessageHandler(Filters.regex('^Создать напоминание$'), self.create_title),
                          MessageHandler(Filters.regex('^Просмотр списка напоминаний$'), self.show_remembral),
                          CallbackQueryHandler(self.create_date_enter_by_hand, pass_user_data=True,
                                               pattern='{}$'.format('ENTER')),
                          CallbackQueryHandler(self.create_date_today, pass_user_data=True,
                                               pattern='{}$'.format('TODAY')),
                          CallbackQueryHandler(self.create_date_calendar, pass_user_data=True,
                                               pattern='{}$'.format('SELECT')),
                          CallbackQueryHandler(self.delete_reminder, pass_user_data=True,
                                               pattern='{}$'.format('DELETE')),
                          CallbackQueryHandler(self.cancel_update_date, pass_user_data=True,
                                               pattern='{}$'.format('CANCEL')),

                          CallbackQueryHandler(self.move_reminder, pass_user_data=True, pattern='{}$'.format('MOVE')),

                          MessageHandler(Filters.text, self.start_after_restart),
                          CallbackQueryHandler(self.change_calendar),
                          ],
            states={
                CHOOSING: [
                    MessageHandler(Filters.regex('^Создать напоминание$'), self.create_title),
                    MessageHandler(Filters.regex('^Просмотр списка напоминаний$'), self.show_remembral),
                    CallbackQueryHandler(self.delete_reminder, pass_user_data=True, pattern='{}$'.format('DELETE')),
                    CallbackQueryHandler(self.move_reminder, pass_user_data=True, pattern='{}$'.format('MOVE')),

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
                    CallbackQueryHandler(self.cancel_update_date, pass_user_data=True, pattern='{}$'.format('CANCEL')),
                    CallbackQueryHandler(self.change_calendar),
                ],
                CHECK_DATE: [
                    MessageHandler(Filters.text, self.check_date)
                ],
                TIME: [
                    MessageHandler(Filters.text, self.check_time)
                ],
            },
            fallbacks=[
                CommandHandler('start', self.start),

            ],
        )

        dispatcher.add_handler(control_handler)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    database = DataBase.DataBase()
    remembrallSettings = RemembrallSettings.RemembrallSettings(database)
    remembrallSettings.first_settings_for_start_server()

    remembrall = Remembrall(database, remembrallSettings)
    remembrall.main(remembrall)

