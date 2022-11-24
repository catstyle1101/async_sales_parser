from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class DatesOfDocuments:
    date_begin: str
    date_end: str


def get_list_of_dates(month: (int | None) = None, increment: int = 3) -> list[DatesOfDocuments]:
    date_pattern = '%d/%m/%y'
    year = datetime.date.today().year
    list_of_dates = list()
    today = datetime.date.today()
    if month:
        today = (datetime.date(year=year, month=(month % 12) + 1, day=1) + datetime.timedelta(days=-1))
    for i in range(1, today.day + 1, increment + 1):
        date_begin = datetime.date(day=i, month=today.month, year=today.year)
        try:
            date_end = datetime.date(day=i+increment, month=today.month, year=today.year)
        except ValueError:
            date_end = datetime.date(year=year, month=(month % 12) + 1, day=1) + datetime.timedelta(days=-1)
        if i + increment > today.day:
            date_end = datetime.date(day=today.day, month=today.month, year=today.year)
        date = DatesOfDocuments(
            date_begin.strftime(date_pattern),
            date_end.strftime(date_pattern),
        )
        list_of_dates.append(date)
    return list_of_dates
