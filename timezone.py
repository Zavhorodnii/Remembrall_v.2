import re
from datetime import datetime, timedelta

import pytz
import tzlocal

time_2 = '8c47'

check = list()
buff = re.split(r'(\d{,2})\D+', time_2)
for i in buff:
    if i != '':
        check.append(8)

user_time_0 = datetime.strptime('2020-03-20 08:31:03', "%Y-%m-%d %H:%M:%S")
# user_time = datetime.utcfromtimestamp(user_time_0)
# print(user_time_0)
print('user_time ', user_time_0)

now_time = datetime.utcnow()
print('now_time ', now_time)

now_date = datetime.now()
step_2 = now_date - timedelta(hours=now_time.hour)
print('step_2 ', step_2)



local_zone = tzlocal.get_localzone()
local_time = user_time_0.astimezone(local_zone)
print('local_time ', local_time)

local_timezone = tzlocal.get_localzone()
print('\nlocal_timezone ', local_timezone)
future_in_half_hour = datetime.now(pytz.utc) - timedelta(hours=user_time_0.hour)
local_time = future_in_half_hour.astimezone(local_timezone)
print('local_time ', local_time)
now_date = datetime.now()
t_3 = datetime.utcnow().replace(tzinfo=pytz.utc)

# if now_date <= now_time:
#     print('Время прошло')


print('t_3 ', t_3)
utctime = datetime.utcnow()
local_time = datetime.now()
print(utctime)
print(local_time)



local_timezone_2 = pytz.timezone("Etc/UTC")
user_time_0 = datetime.strptime('2020-03-20 08:31:03', "%Y-%m-%d %H:%M:%S")
local_timezone = tzlocal.get_localzone()  # pytz-timezone
now = datetime.now()
local_time_ = user_time_0.astimezone(local_timezone_2)
# local_time_ = local_time_ - timedelta(hours=local_timezone.zone)
local_time_3_ = user_time_0.astimezone(local_timezone_2)
local_time_2 = local_time_.astimezone(local_timezone)

user_time_0 = user_time_0.replace(tzinfo=local_timezone)
local_time_ = user_time_0.astimezone(local_timezone_2)
print('gg ', )
print('local_timezone.zone ', pytz.utc)
print('\n\nlocal_timezone ', local_timezone)
print('user_time_0 ', user_time_0)
print('local_time ', local_time)
print('local_time__ ', local_time_)
print('local_time_3_ ', local_time_3_)
print('local_time_2 ', local_time_2)