import json
from typing import cast

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
    TICKER,
    TIMESPAN,
    TO_DATE,
)
from src.data.data_retrieval import CLIENT
from src.data.json_encoder import CustomJSONEncoder


class DataWriter:
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
