from datetime import datetime

import ButtonPressTransfer
import Buttons
import CheckUserData
import TelegramCalendar


class ButtonPressCreate:
    def __init__(self, threads, database, buttons, buttonPressTransfer):
        self.__threads = threads
        self.__database = database
        self.__buttons = buttons
        self.__buttonPressTransfer = buttonPressTransfer
        self.__checkUserData = CheckUserData.CheckUserData()
        self.__date = None
        self.__time = None
        self.__update_rem = None
        self.__context_rem = None

    def create_date_select(self, update):
        update.message.reply_text(
            "Когда должно быть выведено напоминание?\nВыбрать можно на сегодня или позже.",
            reply_markup=self.__buttons.buttons_to_create_date_remem()
        )

    def start_create(self, update, context):
        context.bot.send_message(
            update.effective_chat.id,
            text="Введите заголовок напоминания",
            reply_markup=self.__buttons.remove_button()
        )

    def create_subscribe(self, update, context):
        context.bot.send_message(
            update.effective_chat.id,
            text="Введите текст напоминания"
        )

    def create_date(self, update, context):
        context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Введите дату в формате \'ДД.ММ.ГГ\'"
        )

    def create_date_today(self, update, context):
        dates = self.__checkUserData.create_today()
        self.send_date(update.callback_query.message.chat_id, dates)
        dates = str(dates).split('-')
        dates = '{}.{}.{}'.format(dates[2], dates[1], dates[0])
        self.__date = dates
        context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text='Выбрано дату: ' + dates
        )


    def create_date_calendar(self, update, context):
        context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text=u"Выберите дату",
            reply_markup=self.__buttons.calendar()
        )


    def change_calendar(self, update, context):
        try:
            selected, date_ = TelegramCalendar.process_calendar_selection(context.bot, update)
            if selected:
                self.__date = self.__checkUserData.check_calendar_date(date_)
            context.bot.edit_message_text(
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,
                text="Выбрана дата %s" % (date_.strftime("%d.%m.%Y"))
            )
            date_ = str(date_).split(' ')
            self.send_date(update.callback_query.message.chat_id,date_[0])
            return True
        except Exception as exe:
            return False


    def create_time(self, update, context):
        context.bot.send_message(
            update.effective_chat.id,
            text="Ведите время в формате \'ЧЧ:ММ\'"
        )


    def check_user_date(self, update, context):
        result = self.__checkUserData.check_date(update.message.text)
        if result[0] == 0:
            self.__date = result[1]
            dates = result[1].split('.')
            dates = '{}-{}-{}'.format(dates[2], dates[1], dates[0])
            self.send_date(update.message.from_user.id, dates)
            return True
        else:
            self.send_mess(update, context, result[1])
            return False


    def check_user_time(self, update, context):
        try:
            result = self.__checkUserData.check_time(update.message.text)
            if result[0] == 0:
                if self.__date is None:
                    self.__date = self.__database.last_date_remember(update.message.from_user.id)
                    dates = self.__date.split('-')
                    self.__date = '{}.{}.{}'.format(dates[2], dates[1], dates[0])
                self.__time = result[1]
                times = '{}:00'.format(result[1])
                self.__update_rem = update
                self.__context_rem = context
                self.send_time(update.message.from_user.id, times)
                return True
            else:
                self.send_mess(update, context, result[1])
                return False
        except Exception as exe:
            pass


    def send_mess(self, update, context, mess):
        context.bot.send_message(
            update.effective_chat.id,
            text=mess
        )

    def send_title(self, update):
        try:
            self.__database.send_title(update.message.from_user.id, update.message.text)
        except Exception as exe:
            pass

    def send_subscribe(self, update):
        try:
            self.__database.send_subscribe(update.message.from_user.id, update.message.text)
        except Exception as exe:
            pass


    def send_date(self, user_id, dates):
        try:
            editing = self.__database.check_editing_reminder(user_id)
            if editing == 0:
                self.__database.send_date(user_id, dates)
            else:
                self.__database.send_date_after_transfer(user_id, dates)
        except Exception as exe:
            pass


    def send_time(self, user_id, times):
        try:
            editing = self.__database.check_editing_reminder(user_id)
            if editing == 0:
                self.__database.send_time(user_id, times)
                self.__threads.add_datetime_for_dict_remind(user_id)
            else:
                self.__database.send_time_after_transfer(user_id, times)
                self.__buttonPressTransfer.update_reminder_message(self.__update_rem, self.__context_rem, user_id)
        except Exception as exe:
            pass


    def successful_create_rem(self, update, context):
        context.bot.send_message(
            update.effective_chat.id,
            text="Напоминание появится {} в {}\n {}".format(self.__date, self.__time, datetime.now()),
            reply_markup=self.__buttons.main_button()
        )
