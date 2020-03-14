from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def main_button():
    __reply_keyboard = [
                ['Создать напоминание', 'Просмотр списка напоминаний'],
            ]
    return ReplyKeyboardMarkup(__reply_keyboard, resize_keyboard=True, one_time_keyboard=True)


def remove_button():
    return ReplyKeyboardRemove()

