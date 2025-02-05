import logging

import requests
from polygon import RESTClient

from src.data.constants import POLYGON_API_KEY
from src.data.data_structure import FinancialData

polygon = RESTClient(api_key=POLYGON_API_KEY, trace=True)
data_sources = {'polygon': polygon}


class DataRetrieval:
    def __init__(self, api_key, data_sources):
        self.api_key = api_key
        self.data_sources = data_sources

    def get_data(self, symbol, data_source):
        if data_source in self.data_sources:
            url = self.data_sources[data_source].format(symbol, self.api_key)
            return requests.get(url).json()
        else:
            raise ValueError('Invalid data source')

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
