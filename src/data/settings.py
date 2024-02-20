import os

POLYGON_API_URL = 'https://api.polygon.io/v3/reference/exchanges?asset_class=stocks&apiKey=sTGhTWuYpxCePcrjAfY1N0mnouaLRyOW'
POLYGON_API_KEY = 'sTGhTWuYpxCePcrjAfY1N0mnouaLRyOW'
AGG_FILE_PATH = os.path.abspath('src/data/aggregates_data.json')
EXCH_FILE_PATH = os.path.abspath('src/data/exchanges_data.json')
TICKER = 'AAPL'
MULTIPLIER = 1
TIMESPAN = 'day'
FROM_DATE = '2022-04-01'
TO_DATE = '2022-04-04'
