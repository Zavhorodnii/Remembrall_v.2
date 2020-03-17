from calendar import monthrange
import re

from datetime import datetime

save_date = None


def check_date(text):
    try:
        check = list()
        buff = re.split(r'(\d{,2})\D+', text)
        for i in buff:
            if i != '':
                check.append(i)
        len_2 = len(check)
        if len_2 < 3 or len_2 > 3:
            raise Exception('Неверный формат ввода даты')
        for date in check:
            if date == '':
                raise Exception('Неверный формат ввода даты')

        day = int(check[0])
        month = int(check[1])

        if len(check[2]) > 2:
            raise Exception('Не верный формат ввода года')
        if len(check[2]) < 2:
            check[2] += '0'
        year = int('20' + check[2])
        if day < 1 or month < 1 or year < 1:
            raise Exception('Неверный формат ввода даты')

        if month > 12:
            raise Exception('Неверный формат ввода месяца')

        user_date = datetime.strptime(str(year) + str(month) + str(day), '%Y%m%d').date()

        now = datetime.now().date()
        if user_date < now:
            raise Exception('День уже прошел')
        day_end = monthrange(year, month)
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
        save_date = user_date
        return 0, date
    except Exception as ex:
        return 1, str(ex)


def check_time(time_2):
    try:
        check = list()
        buff = re.split(r'(\d{,2})\D+', time_2)
        for i in buff:
            if i != '':
                check.append(i)
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
        user_time = datetime.strptime(str(hour) + ':' + str(minute) + ':' + '00', "%H:%M:%S").time()
        user_date = datetime.strptime(str(save_date), '%Y-%m-%d').date()

        now_time = datetime.now().time()
        now_date = datetime.now().date()

        if user_date == now_date:
            if user_time <= now_time:
                raise Exception('Время прошло')

        if len(str(hour)) < 2:
            hour = "0{}".format(hour)
        if len(str(minute)) < 2:
            minute = "0{}".format(minute)
        time = "{}:{}".format(hour, minute)
        return 0, time
    except Exception as ex:
        return 1, str(ex)


def create_today():
    global save_date
    save_date = datetime.now().date()
    return save_date


def check_calendar_date(calendar_date):
    calendar_date_ = str(calendar_date).split(' ')
    global save_date
    save_date = calendar_date_[0]
    calendar_date_ = calendar_date_[0].split('-')
    return '{}.{}.{}'.format(calendar_date_[2], calendar_date_[1], calendar_date_[0])
