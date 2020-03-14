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
                                         "FOREIGN KEY (IdRemember) REFERENCES remember(IdRemember))"
        self.__add_title = "INSERT remember (IdUser, TitleRemember, StepCreate) VALUE (%s, %s, %s); "
        self.__last_rem = "select MAX(IdRemember) from remember where IdUser = %s; "
        self.__add_subscribe = "update remember set SubscribeRemember = %s, StepCreate = %s where IdRemember = %s;"
        self.__add_date = "update remember set DateRemember = %s, StepCreate = %s where IdRemember = %s;"
        self.__add_time = "update remember set TimeRemember = %s, StepCreate = %s where IdRemember = %s;"


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

    def send_title(self, id_user, title):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__add_title, (id_user, title, '3'))

    def send_subscribe(self, id_user, subscribe):
        print(id_user)
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem, id_user)
            __id_mess = __con.fetchone()
            __con.execute(self.__add_subscribe, (subscribe, '2', __id_mess))

    def send_date(self, id_user, datetime):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem, id_user)
            __id_mess = __con.fetchone()
            __con.execute(self.__add_date, (datetime, '1', __id_mess))

    def send_time(self, id_user, datetime):
        with self.__my_db_connector:
            __con = self.__my_db_connector.cursor()
            __con.execute(self.__last_rem, id_user)
            __id_mess = __con.fetchone()
            __con.execute(self.__add_time, (datetime, '0', __id_mess))
