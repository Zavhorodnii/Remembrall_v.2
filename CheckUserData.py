from calendar import monthrange
import re

from future.backports.datetime import datetime

save_date = None


def check_date(text):
    try:
        text_2 = re.sub(r'\s+', '', text)
        text_2.strip()
        check = text_2.split('.')
        len_2 = len(check)
        if len_2 < 3 or len_2 > 3:
            raise Exception('Неверный формат ввода даты')
        for date in check:
            if date == '':
                raise Exception('Неверный формат ввода даты')

        day = int(check[0])
        month = int(check[1])
        year = int(check[2])

        if day < 1 or month < 1 or year < 1:
            raise Exception('Неверный формат ввода даты')

        if month > 12:
            raise Exception('Неверный формат ввода месяца')

        if len(check[2]) > 2:
            raise Exception('Не верный формат ввода года')
        if len(check[2]) < 2:
            year *= 10
        now = datetime.now()
        if day < now.day and month <= now.month and year <= now.year:
            raise Exception('День уже прошел')
        new_year = int('20{}'.format(year))
        day_end = monthrange(new_year, month)
        if day > day_end[1]:
            raise Exception('Неверный формат ввода дня')
        day_str = str(day)
        if day < 10:
            day_str = '0{}'.format(day)
        month_str = str(month)
        if month < 10:
            month_str = '0{}'.format(month)

        date = "{}.{}.{}".format(day_str, month_str, year)
        global save_date
        save_date = date
        return 0, date
    except Exception as ex:
        return 1, str(ex)


def check_time(time_2):
    try:
        time = str(time_2)
        text_2 = re.sub(r'\s+', '', time)
        text_2.strip()
        check = text_2.split(':')
        if len(check) < 2 or len(check) > 2:
            raise Exception("Неверный формат ввода времени")
        if not check[0].isdigit() and not check[0].isdigit():
            raise Exception('Неверный формат ввода времени')
        else:
            hour = int(check[0])
        if not check[1].isdigit():
            raise Exception('Неверный формат ввода времени')
        else:
            minute = int(check[1])
        if hour < 0 or hour > 23:
            raise Exception('Неверный формат ввода часов')
        if minute < 0 or minute > 59:
            raise Exception('Неверный формат ввода минут')
        global save_date
        date = save_date.split('.')
        now = datetime.now()
        if int(date[0]) == now.day and int(date[1]) == now.month and int('20{}'.format(date[2])) == now.year:
            if hour <= now.hour and minute <= now.minute:
                raise Exception('Время прошло')

        if len(str(hour)) < 2:
            hour = "0{}".format(hour)
        if len(str(minute)) < 2:
            minute = "0{}".format(minute)
        time = "{}:{}".format(hour, minute)
        return 0, time
    except Exception as ex:
        return 1, str(ex)
