import json
import os
from typing import cast

from polygon import RESTClient
from polygon.rest import models
from urllib3 import HTTPResponse

polygon_api_key = "sTGhTWuYpxCePcrjAfY1N0mnouaLRyOW"
file_path = os.path.abspath("src/data/data.json")
ticker = "AAPL"
multiplier = 1
timespan = "day"
from_date = "2022-04-01"
to_date = "2022-04-04"


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return {"{}".format(o.__class__.__name__): o.__dict__}


def get_aggregates(client: RESTClient):
    return cast(
        HTTPResponse,
        client.get_aggs(ticker, multiplier, timespan, from_date, to_date, raw=False),
    )


def fetch_data(file_path: str):
    client = RESTClient(api_key=polygon_api_key)

    aggs = get_aggregates(client)

    serialized = json.dumps(aggs, indent=4, cls=CustomJSONEncoder)
    print(serialized)

    with open(file_path, "w") as f:
        f.write(serialized)
        print(f"Data successfully written to {file_path}")


if __name__ == "__main__":
    fetch_data(file_path)
