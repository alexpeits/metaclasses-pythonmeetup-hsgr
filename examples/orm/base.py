class ValidationError(Exception):
    """Raised in case of invalid value."""
    pass


class BaseDescriptor(object):
    def __get__(self, obj, cls):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.name]
        except KeyError:
            raise AttributeError('attribute {} not in {}'.format(self.name, obj))

    def __set__(self, obj, val):
        obj.__dict__[self.name] = val


class Field(BaseDescriptor):
    _type = None
    _validators = []

    def __init__(self, description='', validators=None):
        self.description = description
        self.name = None
        if validators is not None:
            self._validators = [*self._validators, *validators]

    def __set__(self, obj, val):
        self.validate(val)
        super().__set__(obj, val)

    def validate_type(self, val):
        return isinstance(val, self._type)

    def validate(self, val):
        if not self.validate_type(val):
            raise ValidationError('incorrect type for value {}'.format(val))
        if not all(v(val) is True for v in self._validators):
            raise ValidationError('invalid value')


class ModelMeta(type):
    """Metaclass for models."""

    def __new__(cls, name, bases, attrs):
        _fields = []
        for k, v in attrs.items():
            if isinstance(v, Field):
                v.name = k
                _fields.append(k.strip('_'))  # like django
        attrs['_fields'] = _fields
        return super().__new__(cls, name, bases, attrs)


class Model(metaclass=ModelMeta):
    """Base class for representing a db table."""

    def __init__(self, **kwargs):
        fields = self._fields
        for k, v in kwargs.items():
            if k not in fields:
                raise ValueError('{} not declared'.format(k))
            setattr(self, k, v)  # <Field>.__set__
