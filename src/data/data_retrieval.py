import json
from typing import cast

import requests
from polygon import RESTClient
from polygon.rest import models
from urllib3 import HTTPResponse

from src.data.constants import (
    AGG_FILE_PATH,
    EXCH_FILE_PATH,
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

    def get_aggregates(self, client: RESTClient):
        return cast(
            HTTPResponse,
            client.get_aggs(
                TICKER, MULTIPLIER, TIMESPAN, FROM_DATE, TO_DATE, raw=False
            ),
        )

    def get_response(self, api_url: str):
        response = requests.get(api_url)
        return response.json()

    def load_data_to_json_file(self, file_path: str):
        aggs_data = self.get_aggregates(CLIENT)
        exchanges_data = self.get_response(POLYGON_API_EXCHANGES_URL)
        financials_data = self.get_response(POLYGON_API_FINANCIALS_URL)

        if file_path == AGG_FILE_PATH:
            aggregates_serialized = json.dumps(
                aggs_data, indent=4, cls=CustomJSONEncoder
            )

            with open(AGG_FILE_PATH, 'w') as f:
                f.write(aggregates_serialized)
                print(f'Data successfully written to {AGG_FILE_PATH}')

        elif file_path == EXCH_FILE_PATH:
            exchanges_serialized = json.dumps(exchanges_data, indent=4)

            with open(EXCH_FILE_PATH, 'w') as f:
                f.write(exchanges_serialized)
                print(f'Data successfully written to {EXCH_FILE_PATH}')

        financials_serialized = json.dumps(financials_data, indent=4)

        with open(FINA_FILE_PATH, 'w') as f:
            f.write(financials_serialized)
            print(f'Data successfully written to {FINA_FILE_PATH}')