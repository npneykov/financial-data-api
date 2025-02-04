import json

from src.data.constants import TICKER


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return {TICKER.format(o.__class__.__name__): o.__dict__}
