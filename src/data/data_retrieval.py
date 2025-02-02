import json
from typing import cast

import requests
from polygon import RESTClient
from polygon.rest import models
from urllib3 import HTTPResponse

from src.data.constants import (
    AGG_FILE_PATH,
    EXCH_FILE_PATH,
    FILE_PATHS,
    FINA_FILE_PATH,
    FROM_DATE,
    MULTIPLIER,
    POLYGON_API_EXCHANGES_URL,
    POLYGON_API_FINANCIALS_URL,
    POLYGON_API_KEY,
    TICKER,
    TIMESPAN,
    TO_DATE,
)

CLIENT = RESTClient(api_key=POLYGON_API_KEY, trace=True)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return {TICKER.format(o.__class__.__name__): o.__dict__}


class DataRetrieval:
    def __init__(self):
        pass

    def get_response(self, api_url: str):
        return requests.get(api_url).json()

    def write_data_to_json_file(self):
        for file_path in FILE_PATHS:
            if file_path == AGG_FILE_PATH:
                aggs_data = cast(
                    HTTPResponse,
                    CLIENT.get_aggs(
                        TICKER, MULTIPLIER, TIMESPAN, FROM_DATE, TO_DATE, raw=False
                    ),
                )
                with open(file_path, 'w') as f:
                    f.write(json.dumps(aggs_data, indent=4, cls=CustomJSONEncoder))
                    print(f'Data successfully written to {file_path}')
            elif file_path == EXCH_FILE_PATH:
                with open(file_path, 'w') as f:
                    f.write(
                        json.dumps(
                            self.get_response(POLYGON_API_EXCHANGES_URL), indent=4
                        )
                    )
                    print(f'Data successfully written to {file_path}')
            elif file_path == FINA_FILE_PATH:
                with open(file_path, 'w') as f:
                    f.write(
                        json.dumps(
                            self.get_response(POLYGON_API_FINANCIALS_URL), indent=4
                        )
                    )
                    print(f'Data successfully written to {file_path}')
