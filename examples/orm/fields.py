import json

from .base import Field


class IntegerField(Field):
    _type = int


class FloatField(Field):
    _type = float


class StringField(Field):
    _type = str


class BooleanField(Field):
    _type = bool


class ListField(Field):
    _type = list


class PositiveNumberField(Field):

    def validate_type(self, val):
        return val > 0


class PositiveIntegerField(IntegerField, PositiveNumberField):
    pass


class JsonField(Field):

    def validate_type(self, val):
        try:
            json.dumps(val)
            return True
        except TypeError:
            return False
