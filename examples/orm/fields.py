import re
import json

from .base import Field, ValidationError


class IntegerField(Field):
    _type = int


class FloatField(Field):
    _type = float


class BooleanField(Field):
    _type = bool


class ListField(Field):
    _type = list


class PositiveNumberField(Field):

    def validate(self, val):
        if val <= 0:
            raise ValidationError('{} is not > 0'.format(val))
        super().validate(val)


class PositiveIntegerField(IntegerField, PositiveNumberField):
    pass


class StringField(Field):
    _type = str

    def __init__(self, size=None, **kwargs):
        self.size = size

    def validate(self, val):
        super().validate(val)
        if self.size is not None and len(val) > self.size:
            raise ValidationError('{} exceeds max length'.format(val))


class RegexStringField(StringField):

    def __init__(self, pattern, **kwargs):
        self.pattern = re.compile(pattern)
        super().__init__(**kwargs)

    def validate(self, val):
        if not self.pattern.match(val):
            raise ValidationError('{} does not match regex'.format(val))
        super().validate(val)


class JsonField(Field):

    def validate(self, val):
        try:
            json.dumps(val)
        except TypeError:
            raise ValidationError('{} is not json serializable'.format(val))
        super().validate(val)

    def transform_get(self, val):
        return json.loads(val)

    def transform_set(self, val):
        return json.dumps(val)
