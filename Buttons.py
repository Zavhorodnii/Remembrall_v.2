from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

import TelegramCalendar


def main_button():
    __reply_keyboard = [
                ['Создать напоминание', 'Просмотр списка напоминаний'],
            ]
    return ReplyKeyboardMarkup(__reply_keyboard, resize_keyboard=True, one_time_keyboard=True)


def remove_button():
    return ReplyKeyboardRemove()


def buttons_to_create_date_remem():
    __keyboard = [
        [InlineKeyboardButton("Сегодня", callback_data=str('TODAY')),
         InlineKeyboardButton("Выбрать", callback_data=str('SELECT')),
         InlineKeyboardButton("Ввести", callback_data=str('ENTER'))]
    ]
    return InlineKeyboardMarkup(__keyboard)


def calendar():
    return TelegramCalendar.create_calendar()


def button_control_mess():
    __keyboard = [
        [InlineKeyboardButton("Удалить", callback_data=str('DELETE')),
         InlineKeyboardButton("Перенести", callback_data=str('MOVE'))]
    ]
    return InlineKeyboardMarkup(__keyboard)


def transfer_remind():
    __keyboard = [
        [InlineKeyboardButton("Сегодня", callback_data=str('TODAY')),
         InlineKeyboardButton("Выбрать", callback_data=str('SELECT')),
         InlineKeyboardButton("Ввести", callback_data=str('ENTER'))],
        [InlineKeyboardButton("Отмена", callback_data=str('CANCEL')), ]
    ]
    return InlineKeyboardMarkup(__keyboard)
