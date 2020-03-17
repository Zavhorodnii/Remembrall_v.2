import DataBase


class RemembrallSettings:
    def __init__(self, database):
        self.__database = database

    def first_settings_for_start_server(self):
        self.__database.check_or_create_db()


    def step_create(self, update):
        return self.__database.step_create(update.message.from_user.id )