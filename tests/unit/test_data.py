import pytest

from src.data.data_retrieval import DataRetrieval
from src.data.data_structure import FinancialData


@pytest.fixture(
    params=[
        ('AAPL', '2020-01-01', '2020-12-31'),
        ('GOOG', '2020-01-01', '2020-12-31'),
        ('MSFT', '2020-01-01', '2020-12-31'),
    ],
)
def financial_data(request):
    symbol, start_date, end_date = request.param
    return FinancialData(symbol, start_date, end_date)


@pytest.fixture(
    params=[
        ('X-Polygon-API-Key', 'polygon'),
        ('Invalid-Polygon-API-Key', 'polygon'),
        ('X-Polygon-API-Key', 'unsupported_data_source'),
    ],
)
def data_retrieval(request):
    api_key, data_sources = request.param
    return DataRetrieval(api_key, data_sources)


class TestDataRetrieval:
    def test_get_data_valid_api_key_and_symbol(data_retrieval):
        symbol = 'AAPL'
        data = data_retrieval.get_data(symbol, data_retrieval.data_sources)
        assert isinstance(data, dict)

    def test_get_data_invalid_api_key(data_retrieval):
        symbol = 'AAPL'
        with pytest.raises(ValueError):
            data_retrieval.get_data(symbol, data_retrieval.data_sources)

    def test_get_data_invalid_symbol(data_retrieval):
        symbol = ' invalid_symbol'
        with pytest.raises(ValueError):
            data_retrieval.get_data(symbol, data_retrieval.data_sources)

    def test_get_data_data_source_not_supported(data_retrieval):
        symbol = 'AAPL'
        with pytest.raises(ValueError):
            data_retrieval.get_data('unsupported_data_source', symbol)


class TestFinancialData:
    def test_financial_data_init(financial_data):
        assert financial_data.symbol in ['AAPL', 'GOOG', 'MSFT']
        assert financial_data.start_date == '2020-01-01'
        assert financial_data.end_date == '2020-12-31'

    def test_financial_data_to_json(financial_data):
        json_data = financial_data.to_json()
        assert isinstance(json_data, str)
        assert financial_data.symbol in json_data
        assert financial_data.start_date in json_data
        assert financial_data.end_date in json_data

    def test_financial_data_get_historical_data(financial_data):
        historical_data = financial_data.get_historical_data('2020-01-01', '2020-12-31')
        assert isinstance(historical_data, list)
        assert len(historical_data) > 0

    def test_financial_data_get_historical_data_invalid_date_range(financial_data):
        with pytest.raises(ValueError):
            financial_data.get_historical_data('2020-12-31', '2020-01-01')

    def test_financial_data_get_historical_data_unknown_symbol(financial_data):
        financial_data.symbol = 'INVALID_SYMBOL'
        with pytest.raises(ValueError):
            financial_data.get_historical_data('2020-01-01', '2020-12-31')
