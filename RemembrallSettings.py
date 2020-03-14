import DataBase


def first_settings_for_start_server():
    first = DataBase.DataBase()
    first.check_or_create_db()
