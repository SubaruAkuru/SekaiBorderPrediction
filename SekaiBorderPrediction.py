import datetime
from numpy import polyfit


def predict(startDate: datetime.date, endDate: datetime.date, data: dict, line: str) -> float:
    """
    :param startDate: The date that event starts.
    :param endDate: The date that event ends.
    :param data: Border during the event, key(s) should be datetime.datetime *in GMT* and value(s) should be int.
    :param line: the border you want to predict. It can be '100', '200', '300', '400', '500', '1000', '2000', '3000',
    '4000', '5000', '10000', '20000', '30000', '40000', '50000', '100000'.
    :return: The border prediction value in float.
    """
    def dataRead(filename: str):
        with open(filename, 'r') as f:
            return eval(f.read())

    def dayTypes():
        def yesterday(d):
            return datetime.date.fromordinal(datetime.date.toordinal(d) - 1)

        def tomorrow(d):
            return datetime.date.fromordinal(datetime.date.toordinal(d) + 1)

        def isHoliday(d: datetime.date):
            def isShukujitu(d: datetime.date):
                def weekdayToDate(year: int, month: int, ordinal: int, weekday: int):
                    firstDay = datetime.date(year=year, month=month, day=1)
                    return datetime.date(year=year, month=month,
                                         day=(7 + weekday - firstDay.weekday()) % 7 + ordinal * 7 - 6)

                def isEquinox(d: datetime.date):
                    Equinox = {2020: {3: 20, 9: 22}, 2021: {3: 20, 9: 23}, 2022: {3: 21, 9: 23},
                               2023: {3: 21, 9: 23}, 2024: {3: 20, 9: 22}, 2025: {3: 20, 9: 23}}
                    return d.month in (3, 9) and d.day == Equinox[d.year][d.month]

                if d.year == 2020:  # R2
                    immovableFeast = {1: (1,), 2: (11, 23), 4: (29,), 5: (3, 4, 5), 7: (23, 24), 8: (10,), 11: (3, 23)}
                    movableFeast = {1: ((2, 0),), 9: ((3, 0),)}
                elif d.year == 2021:  # R3
                    immovableFeast = {1: (1,), 2: (11, 23), 4: (29,), 5: (3, 4, 5), 7: (22, 23), 8: (8,), 11: (3, 23)}
                    movableFeast = {1: ((2, 0),), 9: ((3, 0),)}
                else:
                    immovableFeast = {1: (1,), 2: (11, 23), 4: (29,), 5: (3, 4, 5), 8: (11,), 11: (3, 23)}
                    movableFeast = {1: ((2, 0),), 7: ((3, 0),), 9: ((3, 0),), 10: ((2, 0),)}
                if d.month in immovableFeast and d.day in immovableFeast[d.month]:
                    return True
                elif d.month in movableFeast and d in [weekdayToDate(d.year, d.month, imf[0], imf[1]) for imf in
                                                       movableFeast[d.month]]:
                    return True
                elif isEquinox(d):
                    return True
                else:
                    return False

            def isNearestHishukujitu(d):
                flag = True
                i = yesterday(d)
                while not (isShukujitu(i) and i.weekday() == 6):
                    if not isShukujitu(i):
                        flag = False
                        break
                    i = yesterday(i)
                return flag

            if d.weekday() >= 5:  # is weekend
                return True
            elif isShukujitu(d):  # is shukujitu
                return True
            elif isNearestHishukujitu(d):  # is the first day that is not a shukujitu after a shukujitu on Sunday
                return True
            elif isShukujitu(yesterday(d)) and isShukujitu(tomorrow(d)):  # both yesterday and tomorrow are shukujitu
                return True
            else:
                return False

        def isVacation(d: datetime.date):
            def isSummerVacation(d: datetime.date):
                return d.month == 7 and d.day >= 20 or d.month == 8 and d.day <= 20

            def isWinterVacation(d: datetime.date):
                return d.month == 12 and d.day >= 24 or d.month == 1 and d.day <= 7

            def isSpringVacation(d: datetime.date):
                return d.month == 3 and d.day >= 25 or d.month == 4 and d.day <= 7

            return isSummerVacation(d) or isWinterVacation(d) or isSpringVacation(d)

        dayDict = {}
        ed = startDate
        while ed != tomorrow(endDate):
            dayDict[ed] = ""
            ed = tomorrow(ed)
        for d in dayDict:
            if isHoliday(d):
                dayDict[d] = "H"
            elif isVacation(d):
                dayDict[d] = "V"
            else:
                dayDict[d] = "W"
            if d == startDate:
                dayDict[d] = "S" + dayDict[d]
            elif d == endDate:
                dayDict[d] = "F" + dayDict[d]
            else:
                dayDict[d] = "M" + dayDict[d]
        return dayDict

    def t_to_process(t: datetime.datetime):
        if t.minute == 0:
            durationHourDict = {"S": 12, "M": 24, "F": 17}
            hp = dataRead("data\\holidayParameters.txt")[line]
            shape = dataRead("data\\aveShapeOf{}.txt".format(line))
            dts = dayTypes()
            dayList = list(dts.keys())
            dayList.sort()
            totalProcess = sum([hp[dts[ty]] for ty in dts])
            startTime = datetime.datetime(year=startDate.year, month=startDate.month, day=startDate.day, hour=7)
            process = 0
            h = datetime.timedelta.total_seconds(t - startTime) // 3600 - 1
            i = 0
            while h >= durationHourDict[dts[dayList[i]][0]]:
                h -= durationHourDict[dts[dayList[i]][0]]
                process += hp[dts[dayList[i]]]
                i += 1
            process += hp[dts[dayList[i]]] * shape[dts[dayList[i]]][int(h)]
            return process / totalProcess
        else:
            t0 = datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour)
            t1 = t0 + datetime.timedelta(hours=1)
            k = t.minute / 60
            if t1 != datetime.datetime(year=endDate.year, month=endDate.month, day=endDate.day, hour=12):
                return t_to_process(t0) * (1 - k) + t_to_process(t1) * k
            else:
                return t_to_process(t0) * (1 - k) + k

    dataList, processList = [0], [0]
    tl = list(data.keys())
    tl.sort()
    for t in tl:
        p = data[t] / t_to_process(t)
        dataList.append(data[t])
        processList.append(t_to_process(t))
        print("{}(BJS): {} → 预测 = {:.0f}".format(t + datetime.timedelta(hours=8), data[t], p))
    k = polyfit(processList, dataList, 1)
    print("参考预测值：{}".format(list(k)[0]))