import logging

import requests
from polygon import RESTClient

from src.data.constants import POLYGON_API_KEY
from src.data.data_structure import FinancialData

CLIENT = RESTClient(api_key=POLYGON_API_KEY, trace=True)


class DataRetrieval:
    def __init__(self):
        pass

    def get_response(self, api_url):
        try:
            data = requests.get(api_url).json()
        except requests.exceptions.RequestException as e:
            logging.error(f'Error fetching data: {e}')
            raise

        try:
            financial_data = FinancialData(
                id=data['id'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                timeframe=data['timeframe'],
                fiscal_period=data['fiscal_period'],
                fiscal_year=data['fiscal_year'],
                cik=data['cik'],
                sic=data['sic'],
                tickers=data['tickers'],
                company_name=data['company_name'],
            )

        except KeyError as e:
            logging.error(f'Error parsing data: {e}')
            raise

        return financial_data
