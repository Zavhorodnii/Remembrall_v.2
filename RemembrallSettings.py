import DataBase


def first_settings_for_start_server():
    first = DataBase.DataBase()
    first.check_or_create_db()


def step_create(update, database):
    return database.step_create(update.message.from_user.id)