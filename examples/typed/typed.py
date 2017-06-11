class TypedDescriptor:
    def __init__(self, name, tp, initval=None):
        self.name = name
        self.tp = tp
        if initval is not None and not isinstance(initval, tp):
            raise TypeError('{} is not of type {}'.format(initval, tp))
        self.initval = initval

    def __get__(self, obj, cls):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.name]
        except KeyError:
            if self.initval is not None:
                return self.initval
            raise AttributeError('attribute {} not in {}'.format(self.name, obj))

    def __set__(self, obj, val):
        if not isinstance(val, self.tp):
            raise TypeError('{} is not of type {}'.format(val, self.tp))
        obj.__dict__[self.name] = val


class TypedMeta(type):
    def __new__(mcls, name, bases, attrs):
        ann = attrs.get('__annotations__', {})
        for k, v in ann.items():
            if k in attrs:
                initval = attrs[k]
            else:
                initval = None
            attrs[k] = TypedDescriptor(name=k, tp=v, initval=initval)
        return super().__new__(mcls, name, bases, attrs)


class Typed(metaclass=TypedMeta):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
