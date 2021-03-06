from datetime import datetime
from threading import Thread
from time import sleep



class Threads:
    def __init__(self, database, buttons):
        self.__database = database
        self.__buttons = buttons
        self.__dict_reminder = dict()
        self.__updater = None

        self.__start_send_reminder = dict()


    def add_datetime_for_dict_remind_after_restart(self, updater_):
        try:
            thread = Thread(target=self.check_reminder)
            thread.start()
            self.__updater = updater_
            all_reminder = self.__database.select_all_reminder_where_step_create_equal_zero()
            for i in all_reminder:
                self.__dict_reminder[i[0]] = (i[1], "{} {}".format(i[4], i[5]))
                if i[1] not in self.__start_send_reminder:
                    self.__start_send_reminder[i[1]] = False
                self.start_thread(i[0], i[1], i[2], i[3])
                sleep(0.1)
        except Exception as exe:
            pass

    def check_reminder(self):
        while True:
            for key in self.__start_send_reminder:
                time = self.__database.allow_transfer_reminder(key)
                if time[0] != 0:
                    self.__start_send_reminder[key] = False
                else:
                    self.__start_send_reminder[key] = True
            sleep(10)



    def del_reminder_from_dict_reminder(self, message_id):
        if message_id not in self.__dict_reminder:
            return
        del self.__dict_reminder[message_id[0]]


    def add_datetime_for_dict_remind(self, user_id):
        message = self.__database.select_one_reminder_where_editing_equal_true(user_id)
        if message is None: #create
            message = self.__database.select_last_remember(user_id)
            self.__dict_reminder[message[0]] = (user_id, "{} {}".format(message[3], message[4]))
            if user_id not in self.__start_send_reminder:
                self.__start_send_reminder[user_id] = False
            self.start_thread(message[0], user_id, message[1], message[2])
        else:
            self.__dict_reminder[message[0]] = (user_id, "{} {}".format(message[4], message[5]))


    def start_thread(self, message_id, user_id, title, subscribe):
        thread = Thread(target=self.create_thread, args=(message_id, user_id, title, subscribe))
        thread.start()


    def create_thread(self, message_id, user_id, title, subscribe):
        while True:
            if message_id not in self.__dict_reminder:
                break
            if not self.__start_send_reminder[user_id]:
                sleep(15)
                continue
            date = datetime.strptime(self.__dict_reminder[message_id][1], "%Y-%m-%d %H:%M:%S")
            if date <= datetime.now():
                date = self.__dict_reminder[message_id][1].split(' ')
                correct_date = str(date[0]).split('-')
                call_reminder = self.__updater.bot.send_message(
                    user_id,
                    text="{}\n{}\nДата {}.{}.{}\nВремя {}".format(title, subscribe, correct_date[2], correct_date[1],
                                                                  correct_date[0], date[1]),
                    reply_markup=self.__buttons.button_control_mess()
                )
                self.__database.add_id_reminder(user_id, call_reminder.message_id, message_id)
                sleep(300)
            else:
                sleep(10)