import requests
from polygon import RESTClient

from src.data.constants import POLYGON_API_KEY

CLIENT = RESTClient(api_key=POLYGON_API_KEY, trace=True)


class DataRetrieval:
    def __init__(self):
        pass

    def get_response(self, api_url: str):
        return requests.get(api_url).json()
