import DataBase


class RemembrallSettings:
    def __init__(self, database):
        self.__database = database

    def first_settings_for_start_server(self):
        try:
            self.__database.check_or_create_db()
        except Exception as exe:
            pass


    def step_create(self, update):
        try:
            return self.__database.step_create(update.message.from_user.id )
        except Exception as exe:
            pass