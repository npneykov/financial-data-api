import unittest

from src.data.data_retrieval import DataRetrieval
from src.data.data_structure import FinancialData


class TestData(unittest.TestCase):
    def test_get_data(self):
        api_key = 'your_api_key_here'
        symbol = 'AAPL'
        data_retrieval = DataRetrieval(api_key)
        data = data_retrieval.get_data(symbol, 'polygon')
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)

    def test_init(self):
        financial_data = FinancialData('AAPL', '2020-01-01', '2020-12-31')
        self.assertEqual(financial_data.symbol, 'AAPL')
        self.assertEqual(financial_data.start_date, '2020-01-01')
        self.assertEqual(financial_data.end_date, '2020-12-31')
