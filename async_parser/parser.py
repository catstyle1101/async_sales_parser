import json
import datetime
import logging
from typing import ValuesView

from config import LOGIN, MAN_ID, BASE_URL
from database.database import DataBase, Prefix
from errors.errors import TooManyDocumentsError
from utils.date_creator import DatesOfDocuments
from sale.sale_calculator import Sale
from database.models import Manager


INDEX_IPRO = 1
INDEX_NUMDOC = 2
INDEX_CLIENT = 5
INDEX_DATE = 6
INDEX_SUM = 14


def check_parsed_data(result: json) -> None:
    """Check json data for too many documents error."""
    if result['userdata']['limit'] == 'yes':
        logging.warning("Слишком много документов, уменьшить интервал для поиска")
        raise TooManyDocumentsError("Слишком много документов в периоде")


def parse_json(json_: list[json], managers_dict: dict[str: Manager], result: dict, check_list: list[str]) -> None:
    """Parse json to list of Sale. Append to check_list documents with author is not manager."""
    check_parsed_data(json_)
    for row in json_['rows']:
        try:
            sum_doc = float(row['cell'][INDEX_SUM])
        except ValueError:
            sum_doc = 0
        prefix = Prefix(row['cell'][INDEX_NUMDOC][:7])
        manager = managers_dict.get(prefix.prefix)
        if manager:
            result[row['id']] = Sale(
                int_number=row['id'],
                number=row['cell'][INDEX_NUMDOC],
                client=row['cell'][INDEX_CLIENT],
                date=datetime.datetime.strptime(row['cell'][INDEX_DATE], '%d/%m/%y'),
                sum_doc=sum_doc,
                ipro=row['cell'][INDEX_IPRO] == 'i',
                manager=manager,
            )
        if not manager.is_manager:
            check_list.append(row['id'])


def create_urls_for_scrap_manager(list_numdoc: list[int]) -> list[str]:
    """Create list of URL to scrap manager of document, when author is not manager."""
    result = list()
    for numdoc in list_numdoc:
        result.append(f'{BASE_URL}cat/data-inv-head.html?login_type=WI&id={numdoc}&d_r=1&_=1615266005774')
    return result


def scrap_manager(data: str) -> Manager:
    """Scrap manager from data."""
    base = DataBase()
    if 'Запись не найдена' in data:
        return 0
    val_manager = data.find('contact_mandetail')
    begin = data.find('(', val_manager) + 1
    end = data.find(')', val_manager)
    return base.get_manager_by_internal_digit_code(int(data[begin:end]))


def process_manager_scrapping(data: list[str], list_of_sales: dict[str: Sale]) -> None:
    """Scrap manager internal name from list HTTP responses."""
    for row in data:
        manager = scrap_manager(row)
        begin = row.find('&ch1=') + 5
        end = row.find('&', begin)
        int_num = row[begin:end]
        sale = list_of_sales.get(int_num)
        if sale:
            sale.manager = manager


def create_urls_for_sales(dates: list[DatesOfDocuments], managers: ValuesView[Manager]):
    """Create list of URLS to scrap sales from WEB application."""
    link = f'{BASE_URL}cat/data-invoice.html?'
    result = list()
    for date in dates:
        for manager in managers:
            url = (
                f'{link}login={LOGIN}&man={MAN_ID}&net=4&org-id=8888&d1={date.date_begin}'
                f'&d2={date.date_end}&status=45&allkl=yes&mycli=no&amper_pay=no&usr-inv-num={manager.prefix}'
                f'&_search=true&nd=1591775388995&rows=200&page=1&sidx=inv-date&sord=desc&_=1591775388998'
            )
            result.append(url)
    return result


def create_url_find_manager(numdoc: int):
    """Create URL to scrap true manager of document."""
    return f'{BASE_URL}cat/data-inv-head.html?login_type=WI&id={numdoc}&d_r=1&_=1615266005774'
