# import datetime

# print("\n--------datetime.datetime--------\n")

# xtime = datetime.datetime.now()

# print("now():\t\t", xtime)                      # now():           2023-03-29 23:30:25.248756
# print("type():\t\t", type(xtime))               # type():          <class 'datetime.datetime'>

# print("\n--------Property--------\n")

# print("year:\t\t", xtime.year)                  # year:            2023
# print("month:\t\t", xtime.month)                # month:           3
# print("day:\t\t", xtime.day)                    # day:             29
# print("hour:\t\t", xtime.hour)                  # hour:            23
# print("minute:\t\t", xtime.minute)              # minute:          30
# print("second:\t\t", xtime.second)              # second:          25
# print("microsecond():\t", xtime.microsecond)    # microsecond():   248756

# print("max():\t\t", xtime.max)                  # max():           9999-12-31 23:59:59.99999
# print("min():\t\t", xtime.min)                  # min():           0001-01-01 00:00:00

# print("\n--------Method--------\n")

# print("date():\t\t", xtime.date())              # date():          2023-03-2
# print("time():\t\t", xtime.time())              # time():          23:30:25.248756
# print("weekday():\t", xtime.weekday())          # weekday():       2

# import datetime
# print("\n--------Create Date Object--------\n")
# xtime = datetime.datetime(2020, 5, 17)

# print("datetime()\t", xtime)                # datetime()       2020-05-17 00:00:00
# print("type():\t\t", type(xtime))           # type():          <class 'datetime.datetime'>

import datetime
print("\n--------Format a Date Object--------\n")

xtime = datetime.datetime(2023, 3, 29)

print("now()", xtime)
print("%a:\t", xtime.strftime("%a"))        # %a:      Wed
print("%A:\t", xtime.strftime("%A"))        # %A:      Wednesday
print("%w:\t", xtime.strftime("%w"))        # %w:      3
