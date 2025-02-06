import unittest

from src.data.data_retrieval import DataRetrieval
from src.data.data_structure import FinancialData


class TestData(unittest.TestCase):
    def test_get_data(self):
        api_key = 'POLYGON_API_KEY'
        symbol = 'AAPL'
        data_retrieval = DataRetrieval(api_key)
        data = data_retrieval.get_data(symbol, 'polygon')
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)

    def test_get_data_invalid_api_key(self):
        api_key = 'invalid_api_key'
        symbol = 'AAPL'
        data_retrieval = DataRetrieval(api_key)
        with self.assertRaises(ValueError):
            data_retrieval.get_data(symbol, 'polygon')

    def test_get_data_invalid_symbol(self):
        api_key = 'your_api_key_here'
        symbol = ' invalid_symbol'
        data_retrieval = DataRetrieval(api_key)
        with self.assertRaises(ValueError):
            data_retrieval.get_data(symbol, 'polygon')

    def test_get_data_data_source_not_supported(self):
        api_key = 'your_api_key_here'
        symbol = 'AAPL'
        data_retrieval = DataRetrieval(api_key)
        with self.assertRaises(ValueError):
            data_retrieval.get_data(symbol, 'unsupported_data_source')

    def test_financial_data_init(self):
        symbol = 'AAPL'
        start_date = '2020-01-01'
        end_date = '2020-12-31'
        financial_data = FinancialData(symbol, start_date, end_date)
        self.assertEqual(financial_data.symbol, symbol)
        self.assertEqual(financial_data.start_date, start_date)
        self.assertEqual(financial_data.end_date, end_date)

    def test_financial_data_to_json(self):
        symbol = 'AAPL'
        start_date = '2020-01-01'
        end_date = '2020-12-31'
        financial_data = FinancialData(symbol, start_date, end_date)
        json_data = financial_data.to_json()
        self.assertIsInstance(json_data, str)
        self.assertIn(symbol, json_data)
        self.assertIn(start_date, json_data)
        self.assertIn(end_date, json_data)
