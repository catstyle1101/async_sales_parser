import datetime
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from statistics import median

from database.database import DataBase

from database.models import Manager


class Specialisation(namedtuple('Specialisation', 'name threshold'), Enum):
    RETAIL_MANAGER = 'РМОПП', 15000
    PRIVATE_CLIENT = 'ООК', 15000
    B2B_CLIENT = 'МОПП', 50000


@dataclass()
class Sale:
    int_number: str
    number: str
    client: str
    date: datetime.datetime
    sum_doc: float
    ipro: bool
    manager: Manager


def calculate_sales(data: list[Sale]) -> dict:
    """Calculate a dictionary of all sales, group by manager
    result: {'manager_1_name': {'client_1_name': sum_of_sales_1, 'client_2_name': sum_of_sales_2 ...},
    'manager_2_name': {...} ...} ."""
    result = dict()
    for sale in data:
        if result.get(sale.manager):
            if result[sale.manager].get(sale.client):
                result[sale.manager][sale.client] += int(sale.sum_doc)
            else:
                result[sale.manager].update({sale.client: int(sale.sum_doc)})
        else:
            result[sale.manager] = {sale.client: int(sale.sum_doc)}
    return result


def calculate_rating(manager_sales: dict) -> dict:
    """Calculate sum, median, count buying customer for managers
    buying customer counts with different thresholds for different managers specialisation
    result: {'manager_1_name': ['client_1': sum_of_sales_1, 'client_2': sum_of_sales_2], 'manager_2_name': ...}."""
    result = dict()
    base = DataBase()
    for manager, sales in manager_sales.items():
        man = base.get_manager_by_short_name(str(manager))
        if man.specialization == Specialisation.RETAIL_MANAGER.name:
            pkb_value = Specialisation.RETAIL_MANAGER.threshold
        elif man.specialization == Specialisation.PRIVATE_CLIENT.name:
            pkb_value = Specialisation.PRIVATE_CLIENT.threshold
        else:
            pkb_value = Specialisation.B2B_CLIENT.threshold

        result[manager] = {
          'summa': sum(sales.values()),
          'median': int(median(sales.values())),
          'pkb': len([i for i in sales.values() if i > pkb_value]),
                         }
    return _sort_sales(result)


def _sort_sales(result: dict) -> dict:
    """Sort dictionary by sum of sales."""
    sorted_keys = sorted(result, key=lambda x: result[x]['summa'], reverse=True)
    sorted_sales = dict()
    for item in sorted_keys:
        sorted_sales[item] = result[item]
    return sorted_sales


def calculate_full_rating(data: list[Sale]):
    manager_sales = calculate_sales(data)
    data_for_rating = calculate_rating(manager_sales)
    return data_for_rating
