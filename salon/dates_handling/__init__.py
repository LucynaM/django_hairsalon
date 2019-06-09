import datetime


def get_dates():
    """get dates range for search form"""
    my_date = datetime.date.today()
    num = 0
    for i in range(0, 28, 7):
        # 4 weeks start-end dates
        start = my_date + datetime.timedelta(days=i)
        end = start + datetime.timedelta(days=6)
        if start.year == end.year and start.month == end.month:
            start = start.strftime('%d.')
        elif start.year == end.year:
            start = start.strftime('%d.%m.')
        else:
            start = start.strftime('%d.%m.%Y')
        end = end.strftime('%d.%m.%Y')
        yield (num, '{}-{}'.format(start, end))
        num += 1


def get_absences(users):
    """get staff absences days"""
    absences = {}
    for user in users:
        absences[user] = []
        for absence in user.absences.all():
            day_range = absence.end - absence.start
            day_range_as_num = day_range.days
            for i in range(0, day_range_as_num + 1):
                absences[user].append(absence.start + datetime.timedelta(days=i))
    return absences


def get_absence_days(absence):
    """get absence days"""
    day_range = absence.end - absence.start
    day_range_as_num = day_range.days
    for i in range(0, day_range_as_num + 1):
        yield absence.start + datetime.timedelta(days=i)


def get_haircuts(users):
    """ get staff occupied hours """
    haircuts = {}
    for user in users:
        haircuts[user] = []
        for haircut in user.services.filter(date__gte=datetime.datetime.now()):
            hour_range = int(haircut.service.duration / 60)
            for i in range(0, hour_range):
                haircuts[user].append(haircut.date.replace(tzinfo=None) + datetime.timedelta(hours=i))
    return haircuts


def get_calendar(day_choice, holidays):
    """ days without sundays and holidays """
    date = datetime.datetime.now().replace(hour=11, minute=00, second=00, microsecond=000000) + datetime.timedelta(days=7*day_choice)
    for day_offset in range(0, 7):
        day = date + datetime.timedelta(days=day_offset)
        if day.weekday() != 6 and day.date() not in holidays:
            yield day


def get_hours_needed(service_duration, day_hour):
    """ split service duration into hours """
    return [day_hour + datetime.timedelta(hours=i) for i in range(0, service_duration)]


def get_user_calendar(day_choice,
                      holidays,
                      user,
                      absences,
                      haircuts,
                      start_hour,
                      end_hour,
                      service_duration):
    calendar = get_calendar(day_choice, holidays)
    hours = []
    for day in calendar:
        if day.date() not in absences[user]:
            for hour_offset in range(start_hour, end_hour):
                hours.append(day + datetime.timedelta(hours=hour_offset))

    return (hour for hour in hours
            if len([True for item in get_hours_needed(service_duration, hour)
                   if item not in haircuts[user] and item < hour.replace(hour=19)]) == len(get_hours_needed(service_duration, hour))
            and hour > datetime.datetime.now())


def return_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')