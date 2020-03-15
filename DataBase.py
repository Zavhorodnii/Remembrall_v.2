import pymysql as pymysql


class DataBase:
    def __init__(self):
        self.__my_db_connector = pymysql.connect(
            'localhost',
            'root',
            'Ambrasador83',
            'remembrall_v2'
        )
        # self.__my_db_connector = None
        self.__check_or_create_database = "CREATE DATABASE IF NOT EXISTS Remembrall_v2"
        self.__create_db_table_settings = "CREATE TABLE IF NOT EXISTS settings(" \
                                          "IdUser INT PRIMARY KEY," \
                                          "IntervalRepeat TIME DEFAULT '00:05:00'," \
                                          "CountRepeat INT NULL)"
        self.__create_db_table_remember = "CREATE TABLE IF NOT EXISTS remember(" \
                                          "IdRemember INT AUTO_INCREMENT PRIMARY KEY," \
                                          "IdUser INT," \
                                          "TitleRemember TEXT," \
                                          "SubscribeRemember TEXT," \
                                          "DateRemember DATE," \
                                          "TimeRemember TIME," \
                                          "StepCreate INT)"
        self.__create_db_table_message = "CREATE TABLE IF NOT EXISTS message(" \
                                         "IdMessage INT UNIQUE NOT NULL PRIMARY KEY," \
                                         "IdRemember INT NOT NULL," \
                                         "FOREIGN KEY (IdRemember) REFERENCES remember(IdRemember) on delete cascade)"
        self.__add_title = "INSERT remember (IdUser, TitleRemember, StepCreate) VALUE (%s, %s, %s); "
        self.__last_rem = "select MAX(IdRemember) from remember where IdUser = %s; "
        self.__add_subscribe = "update remember set SubscribeRemember = %s, StepCreate = %s where IdRemember = %s;"
        self.__add_date = "update remember set DateRemember = %s, StepCreate = %s where IdRemember = %s;"
        self.__add_time = "update remember set TimeRemember = %s, StepCreate = %s where IdRemember = %s;"
        self.__step_create = "select StepCreate from remember where IdRemember = (" \
                             "select MAX(IdRemember) from remember where IdUser = %s);"
        self.__last_date_remember = "select DateRemember from remember where IdRemember = (" \
                                    "select MAX(IdRemember) from remember where IdUser = %s);"
        self.__select__oll_remember = "select IdRemember, TitleRemember, SubscribeRemember, DateRemember, " \
                                      "TimeRemember from remember where IdUser=%s"
        self.__add_id_reminder = "INSERT message (IdMessage, IdRemember)" \
                                 "VALUES (%s, %s)"
        self.__select_repeat_message = "select IdMessage from message where IdRemember = (select " \
                                       "IdRemember from message where IdMessage = %s); "
        self.__delete_reminder = "DELETE FROM remember WHERE IdRemember = (select IdRemember from " \
                                 "message where IdMessage = %s)"

    def check_or_create_db(self):
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="Ambrasador83"
        )
        with mydb:
            __cur = mydb.cursor()
            __cur.execute(self.__check_or_create_database)
        self.__my_db_connector = pymysql.connect(
            'localhost',
            'root',
            'Ambrasador83',
            'remembrall_v2'
        )
        with self.__my_db_connector:
            __cur = self.__my_db_connector.cursor()
            __cur.execute(self.__create_db_table_settings)
            __cur.execute(self.__create_db_table_remember)
            __cur.execute(self.__create_db_table_message)
            __cur.close()

    def send_title(self, user_id, title):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__add_title, (user_id, title, '3'))

    def send_subscribe(self, user_id, subscribe):
        print(user_id)
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem, user_id)
            __id_mess = __con.fetchone()
            __con.execute(self.__add_subscribe, (subscribe, '2', __id_mess))

    def send_date(self, user_id, datetime):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem, user_id)
            __id_mess = __con.fetchone()
            __con.execute(self.__add_date, (datetime, '1', __id_mess))

    def send_time(self, user_id, datetime):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem, user_id)
            __id_mess = __con.fetchone()
            __con.execute(self.__add_time, (datetime, '0', __id_mess))

    def step_create(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__step_create, user_id)
            step = __con.fetchone()
        return step

    def last_date_remember(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_date_remember, user_id)
            last = __con.fetchone()
        return str(last[0])

    def select_all_remember(self, user_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select__oll_remember, user_id)
            all = __con.fetchall()
        return all

    def add_id_reminder(self, message_id, reminder_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__add_id_reminder, (message_id, reminder_id))

    def select_repeat_message(self, message_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__select_repeat_message, message_id)
            all = __con.fetchall()
        return all

    def delete_reminder(self, message_id):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__delete_reminder, message_id)
