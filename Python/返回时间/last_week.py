import datetime

def get_last_week():

    monday = datetime.date.today() + datetime.timedelta(days = -7)
    sunday = datetime.date.today() + datetime.timedelta(days = -7)

    print(monday)
    print(sunday)

    one_day = datetime.timedelta(days=1)

    print(one_day)
    print(monday.weekday)

    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # 返回当前的星期一和星期天的日期

    print(monday)
    print(sunday)

    return monday, sunday


print(get_last_week())

