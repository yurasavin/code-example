import json
from decimal import Decimal


class DecimalJsonEncoder(json.JSONEncoder):
    """
    JSON Encoder class does Decimal transformation.
    It stores Decimal values using string type instead of float.
    """

    def default(self, obj):
        if isinstance(obj, Decimal):
            return {'$decimal_value': str(obj)}
        return super().default(obj)
