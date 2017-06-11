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

    def __init__(self, description=''):
        self.description = description
        self.name = None

    def __get__(self, obj, cls):
        val = super().__get__(obj, cls)
        return self.transform_get(val)

    def __set__(self, obj, val):
        self.validate(val)
        super().__set__(obj, self.transform_set(val))

    def validate(self, val):
        if self._type is not None and not isinstance(val, self._type):
            raise ValidationError('incorrect type for value {}'.format(val))

    def transform_get(self, val):
        return val

    def transform_set(self, val):
        return val


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

    def __repr__(self):
        name = self.__class__.__name__
        fields = []
        for f in self._fields:
            if f in self.__dict__:
                val = self.__dict__[f]
                fields.append('{}={}'.format(f, val))
        return '{}({})'.format(name, ', '.join(fields))
