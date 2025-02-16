from datetime import datetime, timedelta

import pytest

from src.data.constants import DATA_FILE_PATH
from src.data.data_retrieval import DataRetrieval
from src.data.data_structure import FinancialData
from src.view.data_visualization import DataVisualization


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


@pytest.fixture
def data_visualization():
    return DataVisualization


class TestDataRetrieval:
    def test_data_retrieval_init(data_retrieval):
        assert data_retrieval.api_key in data_retrieval.api_key
        assert data_retrieval.data_sources in data_retrieval.data_sources

    def test_get_data_with_valid_api_key_and_symbol(data_retrieval):
        symbol = 'AAPL'
        data = data_retrieval.get_data(symbol, data_retrieval.data_sources)
        assert isinstance(data, dict)

    def test_get_data_with_invalid_api_key(data_retrieval):
        api_key = 'Invalid-Polygon-API-Key'
        symbol = 'AAPL'
        with pytest.raises(ValueError):
            data_retrieval.get_data(symbol, data_retrieval.data_sources)
        assert api_key not in data_retrieval.api_key

    def test_get_data_with_invalid_symbol(data_retrieval, financial_data):
        symbol = ' invalid_symbol'
        with pytest.raises(ValueError):
            data_retrieval.get_data(symbol, data_retrieval.data_sources)
        assert symbol not in financial_data.symbol

    def test_get_data_with_empty_symbol(data_retrieval):
        with pytest.raises(ValueError) as e:
            data_retrieval.get_data('', data_retrieval.data_sources)
        assert str(e.value) == 'Symbol cannot be empty'

    def test_get_data_with_none_symbol(data_retrieval):
        with pytest.raises(ValueError) as e:
            data_retrieval.get_data(None, data_retrieval.data_sources)
        assert str(e.value) == 'Symbol cannot be None'

    def test_get_data_data_source_not_supported(data_retrieval):
        symbol = 'AAPL'
        with pytest.raises(ValueError) as e:
            data_retrieval.get_data(symbol, 'unsupported_data_source')
        assert str(e.value) == 'Invalid data source'

    def test_data_retrieval_api_request_failure(data_retrieval):
        with pytest.raises(ValueError) as e:
            data_retrieval.get_data('AAPL', 'polygon')
        assert str(e.value) == 'Error fetching data'

    def test_data_retrieval_api_rate_limit(data_retrieval):
        with pytest.raises(ValueError) as e:
            data_retrieval.get_data('AAPL', 'polygon')
        assert 'Rate limit exceeded' in str(e.value)

    def test_data_retrieval_large_datasets(data_retrieval):
        data = data_retrieval.get_data('AAPL', 'polygon')
        assert isinstance(data, dict)
        assert len(data) > 1000

    def test_data_retrieval_timeout_handling(data_retrieval, mocker):
        mocker.patch('requests.get', side_effect=TimeoutError)
        with pytest.raises(TimeoutError):
            data_retrieval.get_data('AAPL', 'polygon')


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
        financial_data.end_date = '2020-01-01'
        financial_data.start_date = '2020-12-31'
        with pytest.raises(ValueError):
            financial_data.get_historical_data(
                financial_data.start_date,
                financial_data.end_date,
            )
        assert financial_data.start_date > financial_data.end_date

    def test_financial_data_get_historical_data_invalid_symbol(financial_data):
        financial_data.symbol = 'INVALID_SYMBOL'
        with pytest.raises(ValueError):
            financial_data.get_historical_data('2020-01-01', '2020-12-31')
        assert financial_data.symbol == 'INVALID_SYMBOL'

    def test_financial_data_get_historical_data_empty_list(financial_data):
        historical_data = financial_data.get_historical_data('2020-01-01', '2020-12-31')
        assert isinstance(historical_data, list)
        assert len(historical_data) == 0

    def test_financial_data_with_invalid_symbol(financial_data):
        financial_data.symbol = 'INVALID_SYMBOL'
        with pytest.raises(ValueError):
            financial_data.to_json()
        assert financial_data.symbol == 'INVALID_SYMBOL'

    def test_financial_data_with_empty_start_date(financial_data):
        financial_data.start_date = ''
        with pytest.raises(ValueError):
            financial_data.to_json()
        assert financial_data.start_date == ''

    def test_financial_data_with_none_start_date(financial_data):
        financial_data.start_date = None
        with pytest.raises(ValueError):
            financial_data.to_json()
        assert financial_data.start_date is None

    def test_financial_data_with_different_date_formats(financial_data):
        financial_data.start_date = '2020-01-01T00:00:00Z'
        financial_data.end_date = '2020-12-31T23:59:59Z'
        json_data = financial_data.to_json()
        assert '2020-01-01T00:00:00Z' in json_data

    def test_financial_data_future_date_request(financial_data):
        future_date = datetime.now() + timedelta(days=1)
        with pytest.raises(ValueError):
            financial_data.test_financial_data_get_historical_data(
                '2020-01-01', future_date,
            )


class TestDataVisualization:
    def test_data_visualization_init(data_visualization):
        assert isinstance(data_visualization, DataVisualization)

    def test_data_visualization_plot_data_invalid_file_path(data_visualization):
        with pytest.raises(ValueError):
            data_visualization.plot_data('invalid_file_path')
        assert data_visualization.file_path != 'invalid_file_path'

    def test_data_visualization_plot_data_valid_file_path(data_visualization):
        assert data_visualization.plot_data(
            DATA_FILE_PATH,
        ) == data_visualization.plot_data('src/data/json/data.json')

    def test_data_visualization_plot_data_none_file_path(data_visualization):
        with pytest.raises(ValueError):
            data_visualization.plot_data(None)
        assert data_visualization.file_path is None

    # TODO: Add more test cases for the data visualization class
