import logging
import sys

from dotenv import load_dotenv

from async_parser.parse_async import scrap_urls
from async_parser.parser import (create_urls_for_sales,
                                 create_urls_for_scrap_manager, parse_json,
                                 process_manager_scrapping)
from config import DATE_INCREMENT
from database.database import DataBase
from sale.sale_calculator import calculate_full_rating
from sale.sale_formatter import format_data_rating
from utils.date_creator import get_list_of_dates
from utils.timer import timer


@timer
def main():
    """
    Создает рейтинг продаж менеджеров до определенной даты.

    Использование:
    python main.py - рейтинг до текущей даты
    python main.py 1 - выгрузка продаж определенного месяца
    """
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else None
    load_dotenv()
    create_logger()
    base = DataBase()
    list_of_dates = get_list_of_dates(month= arg, increment=DATE_INCREMENT)
    check_list = list()
    list_of_sales = dict()
    managers_dict = {manager.prefix: manager for manager in base.get_all_managers()}
    urls = create_urls_for_sales(list_of_dates, managers_dict.values())
    raw_data = scrap_urls(urls)
    for row in raw_data:
        parse_json(row, managers_dict, list_of_sales, check_list)
    urls_scrap_true_manager = create_urls_for_scrap_manager(check_list)
    raw_data_for_scrap_manager = scrap_urls(urls_scrap_true_manager, to_json=False)
    process_manager_scrapping(raw_data_for_scrap_manager, list_of_sales)
    list_of_true_managers = {i.short_fullname: i for i in base.get_all_true_managers()}
    for sale in list_of_sales.values():
        if sale.manager:
            sale.manager = list_of_true_managers.get(sale.manager.short_fullname)
    calculated_data = calculate_full_rating([i for i in list_of_sales.values() if i.manager])
    formatted_string = format_data_rating(calculated_data)
    print(formatted_string)


def create_logger() -> None:
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(filename='parser.log', encoding='utf-8', mode='a')
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


if __name__ == '__main__':
    main()
