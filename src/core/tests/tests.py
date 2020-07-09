from decimal import Decimal
import json

import pytest

from faker import Faker

from core.viewset_mixins import SerializerMapMixin
from core.utils import DecimalJsonEncoder

faker = Faker()


class TestDecimalJsonEncoder:

    @pytest.mark.parametrize('test_input,expected', [
        (Decimal('1.00'), json.dumps({"$decimal_value": "1.00"})),
        (Decimal('-15.44'), json.dumps({"$decimal_value": "-15.44"})),
        (Decimal('0.99'), json.dumps({"$decimal_value": "0.99"})),
        (Decimal('467152.15'), json.dumps({"$decimal_value": "467152.15"})),
        (Decimal('0'), json.dumps({"$decimal_value": "0"})),
    ])
    def test_serialize_decimal(self, test_input, expected):
        dump = json.dumps(test_input, cls=DecimalJsonEncoder)
        assert dump == expected

    @pytest.mark.parametrize('test_input', ['1.00', 12, 3.14, 'string', True])
    def test_serialize_other_types(self, test_input):
        dump = json.dumps(test_input, cls=DecimalJsonEncoder)
        assert dump == json.dumps(test_input)


class TestSerializerMapMixin:
    class View(SerializerMapMixin):
        serializer_class = 'DefaultSerializer'
        serializer_class_map = {
            'get': 'GetSerializer',
            'list': 'ListSerializer',
        }

        def __init__(self, action):
            self.action = action

    @pytest.mark.parametrize('action,expected_serializer_class', [
        ('get', 'GetSerializer'),
        ('list', 'ListSerializer'),
        ('create', 'DefaultSerializer'),
    ])
    def test_actions(self, action, expected_serializer_class):
        view = self.View(action)
        serializer = view.get_serializer_class()
        assert serializer == expected_serializer_class
