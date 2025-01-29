from bs4 import BeautifulSoup
import requests

from typing import Any, Dict, List, Optional


def get_aggregate(xml_path: str, agg_type: str) -> Dict[str, float]:
    with open(xml_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'xml')
    answer = {}
    positions = soup.find_all('position')
    for position in positions:
        products = position.find_all('product')
        for product in products:
            sum = product.find('sumMax').text
            if agg_type == 'okpd':
                code = product.find('OKPD').find('code').text
                if code not in answer:
                    answer[code] = float(sum)
                else:
                    answer[code] += float(sum)

            if agg_type == 'placing_way':
                code = position.find('placingWay').find('code').text
                if code not in answer:
                    answer[code] = float(sum)
                else:
                    answer[code] += float(sum)

    return answer


def get_position_sums(paths: List[str]) -> List[Dict[str, Optional[str]]]:
    position_sums = []

    for path in paths:
        with open(path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'xml')

        set_of_positions = soup.find_all('position')

        for pos in set_of_positions:
            if pos.find('orderNumber') is not None:
                order_number = pos.find('orderNumber').text
            else:
                order_number = None

            if pos.find('contractMaxPrice') is not None:
                contract_max_price = pos.find('contractMaxPrice').text
            else:
                contract_max_price = None
            if pos.find('placingWay').find('code') is not None:
                placing_way_code = pos.find('placingWay').find('code').text
            else:
                placing_way_code = None
            if pos.find('contractCurrency').find('code') is not None:
                contract_currency = pos.find('contractCurrency').find('code').text
            else:
                contract_currency = None

            sum_max_total = float(0)
            products = pos.find_all('product')
            for product in products:
                if product.find('sumMax') is not None:
                    sum_max = product.find('sumMax').text
                else:
                    sum_max="0"
                sum_max_total += float(sum_max)


            position_sums.append({
                "order_number": order_number,
                "contract_max_price": contract_max_price,
                "placing_way_code": placing_way_code,
                "contract_currency": contract_currency,
                "sum": sum_max_total
            })

    return position_sums

def get_okpd_tree(paths: List[str], okpds: List[str]) -> Dict[str, Any]:
    return {}


def get_okved_tree(paths: List[str], okveds: List[str]) -> Dict[str, Any]:
    return {}