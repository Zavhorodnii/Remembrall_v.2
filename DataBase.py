import psycopg2


class DataBase:
    def __init__(self):
        self.__my_db_connector = psycopg2.connect(
            database="d3gpt2hhblulef",
            user="fbvhrphsyusben",
            password="74c1edc7b999b36d32e87a022429bb1f4a13c2aa3839cb14debcd8abb5f228f1",
            host="ec2-176-34-97-213.eu-west-1.compute.amazonaws.com",
            port="5432"
        )
        self.__create_db_table_settings = "CREATE TABLE IF NOT EXISTS settings(" \
                                          "IdUser INT UNIQUE PRIMARY KEY," \
                                          "IntervalRepeat TIME DEFAULT '00:05:00'," \
                                          "CountRepeat INT NULL)"
        self.__create_db_table_remember = "CREATE TABLE IF NOT EXISTS remember(" \
                                          "IdRemember SERIAL PRIMARY KEY," \
                                          "IdUser INT," \
                                          "TitleRemember TEXT," \
                                          "SubscribeRemember TEXT," \
                                          "DateRemember DATE," \
                                          "TimeRemember TIME," \
                                          "StepCreate INT," \
                                          "Editing bool default false )"
        self.__create_db_table_message = "CREATE TABLE IF NOT EXISTS message(" \
                                         "Id SERIAL PRIMARY KEY," \
                                         "IdUser INT," \
                                         "IdMessage INT NOT NULL ," \
                                         "IdRemember INT NOT NULL," \
                                         "FOREIGN KEY (IdRemember) REFERENCES remember(IdRemember) on delete cascade)"
        self.__add_title = "INSERT INTO remember(iduser, titleremember, stepcreate) VALUES (%(one)s, %(two)s, %(three)s); "
        self.__last_rem = "select MAX(IdRemember) from remember where IdUser = {}; "
        self.__add_subscribe = "update remember set SubscribeRemember = %(one)s, StepCreate = %(two)s where IdRemember = %(three)s;"
        self.__add_date = "update remember set DateRemember = %(one)s, StepCreate = %(two)s where IdRemember = %(three)s;"
        self.__add_time = "update remember set TimeRemember = %(one)s, StepCreate = %(two)s where IdRemember = %(three)s;"
        self.__step_create = "select StepCreate from remember where IdRemember = (" \
                             "select MAX(IdRemember) from remember where IdUser = {});"
        self.__last_date_remember = "select DateRemember from remember where IdRemember = (" \
                                    "select MAX(IdRemember) from remember where IdUser = {});"
        self.__select__all_remember = "select IdRemember, TitleRemember, SubscribeRemember, DateRemember, " \
                                      "TimeRemember from remember where IdUser = {}; "
        self.__add_id_reminder = "INSERT INTO message (IdUser, IdMessage, IdRemember)" \
                                 "VALUES ({}, {}, {})"
        self.__select_repeat_message = "select IdMessage from message where IdRemember = (select " \
                                       "IdRemember from message where IdUser = {} and IdMessage = {}); "
        self.__delete_reminder = "DELETE FROM remember WHERE IdRemember = (select IdRemember from " \
                                 "message where IdUser = {} and IdMessage = {})"
        self.__select_one_reminder_before_delete = "select IdRemember from message where IdUser = {} and IdMessage = {};"
        self.__select_one_reminder = "select IdRemember, TitleRemember, SubscribeRemember, DateRemember, " \
                                     "TimeRemember from remember where IdRemember = (select IdRemember " \
                                     "from message where IdUser = {} and IdMessage = {} );"
        self.__start_editing_reminder = "update remember set Editing = true where IdRemember = (select IdRemember " \
                                        "from message where IdUser = {} and IdMessage = {} );"
        self.__finish_editing_reminder = "update remember set Editing = false where IdRemember = %(one)s;"
        self.__check_editing_reminder = "select count(true) from remember where IdUser = {} and Editing = true;"
        self.__transfer_reminder = "select IdRemember from remember where IdUser = {} and Editing = true;"
        self.__select_one_reminder_where_editing_equal_true = "select IdRemember, IdUser, TitleRemember, SubscribeRemember, " \
                                                              "DateRemember, TimeRemember from remember where IdUser = " \
                                                              "{} and Editing = true"
        self.__select_repeat_message_with_id_remember = "select IdMessage from message where IdUser = {} and " \
                                                        "IdRemember = {}"
        self.__select_last_repeat_message_with_id_reminder = "select max(IdMessage) from message where IdUser = {} " \
                                                             "and IdRemember = {}; "
        self.__select_last_remember = "select IdRemember, TitleRemember, SubscribeRemember, DateRemember, " \
                                       "TimeRemember from remember where IdRemember = (select MAX(IdRemember) from " \
                                       "remember where IdUser = {} and StepCreate = {});"
        self.__select_all_reminder_where_step_create_equal_zero = "select IdRemember, IdUser, TitleRemember, " \
                                                                  "SubscribeRemember, DateRemember, " \
                                                                  "TimeRemember from remember where StepCreate = {};"
        self.__allow_transfer_reminder = "select count(*) from remember where IdUser = {} and StepCreate > {} " \
                                         "or IdUser = {} and Editing = True; "

    def check_or_create_db(self):

        with self.__my_db_connector:
            __cur = self.__my_db_connector.cursor()
            __cur.execute(self.__create_db_table_settings)
            __cur.execute(self.__create_db_table_remember)
            __cur.execute(self.__create_db_table_message)
            __cur.close()

    def send_title(self, user_id, title):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__add_title, {'one': user_id, 'two': title, 'three': '3'})

    def send_subscribe(self, user_id, subscribe):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem.format(user_id))
            __id_mess = __con.fetchone()
            __con.execute(self.__add_subscribe, {'one': subscribe, 'two': '2', 'three': __id_mess})

    def send_date(self, user_id, datetime):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem.format(user_id))
            __id_mess = __con.fetchone()
            __con.execute(self.__add_date, {'one': datetime, 'two': '1',  'three':__id_mess})

    def send_time(self, user_id, datetime):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem.format(user_id))
            __id_mess = __con.fetchone()
            __con.execute(self.__add_time, {'one': datetime, 'two': '0', 'three':__id_mess})

    def step_create(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__step_create.format(user_id))
            step = __con.fetchone()
        return step

    def last_date_remember(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_date_remember.format(user_id))
            last = __con.fetchone()
        return str(last[0])

    def select_all_remember(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select__all_remember.format(user_id))
            all = __con.fetchall()
        return all

    def add_id_reminder(self, user_id, message_id, reminder_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__add_id_reminder.format(user_id, message_id, reminder_id))

    def select_repeat_message(self, user_id, message_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_repeat_message.format(user_id, message_id))
            all = __con.fetchall()
        return all

    def delete_reminder(self, user_id, message_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__delete_reminder.format(user_id, message_id))

    def elect_one_reminder_before_delete(self, user_id, message_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_one_reminder_before_delete.format(user_id, message_id))
            one = __con.fetchone()
        return one

    def select_one_reminder(self, user_id, message_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_one_reminder.format(user_id, message_id))
            one = __con.fetchone()
        return one

    def start_editing_reminder(self, user_id, message_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__start_editing_reminder.format(user_id, message_id))

    def finish_editing_reminder(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__transfer_reminder.format(user_id))
            __id_reminder = __con.fetchone()
            __con.execute(self.__finish_editing_reminder, {'one': __id_reminder})

    def check_editing_reminder(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__check_editing_reminder.format(user_id))
            editing = __con.fetchone()
        return editing[0]

    def send_date_after_transfer(self, user_id, date):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__transfer_reminder.format(user_id))
            __id_reminder = __con.fetchone()
            __con.execute(self.__add_date, {'one': date, 'two': '1', 'three': __id_reminder})

    def send_time_after_transfer(self, user_id, time):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__transfer_reminder.format(user_id))
            __id_reminder = __con.fetchone()
            __con.execute(self.__add_time, {'one': time, 'two': '0', 'three': __id_reminder})

    def select_one_reminder_where_editing_equal_true(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_one_reminder_where_editing_equal_true.format(user_id))
            one = __con.fetchone()
        return one

    def select_repeat_message_with_id_remember(self, user_id, __id_reminder):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_repeat_message_with_id_remember.format(user_id, __id_reminder))
            all = __con.fetchall()
        return all

    def select_last_repeat_message_with_id_reminder(self, user_id, __id_reminder):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_last_repeat_message_with_id_reminder.format(user_id, __id_reminder))
            one = __con.fetchone()
        return one

    def select_last_remember(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_last_remember.format(user_id, '0'))
            one = __con.fetchone()
        return one

    def select_all_reminder_where_step_create_equal_zero(self):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_all_reminder_where_step_create_equal_zero.format('0'))
            all = __con.fetchall()
        return all


    def allow_transfer_reminder(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__allow_transfer_reminder.format(user_id, '0', user_id))
            return __con.fetchone()

