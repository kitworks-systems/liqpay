from collections import MutableMapping
import json
from liqpay.exceptions import ParamValidationError, ParamRequired
from liqpay.settings import SUPPORTED_CURRENCIES, PAY_WAYS


class Params(MutableMapping):
    validators = {
        'public_key': lambda x: x,
        'amount': lambda x: float(x) > 0,
        'description': lambda x: x,
        'currency': lambda x: x in SUPPORTED_CURRENCIES,
        'pay_way': lambda x: x in PAY_WAYS,
    }
    post_processors = {
        'sandbox': lambda x: int(bool(x))
    }

    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._validate(key, value)
        value = self._post_process(key, value)
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __contains__(self, key):
        return key in self._store

    def __str__(self):
        return str(self._store)

    def __repr__(self):
        return repr(self._store)

    def to_json(self):
        return json.dumps(self._store, sort_keys=True, ensure_ascii=False)

    def has_required_fields(self, required_fields):
        return set(required_fields).issubset(self.keys())

    def require_fields(self, fields):
        if not self.has_required_fields(fields):
            raise ParamRequired('Required param(s) not found: "{}"'.format(
                ', '.join(set(fields) - set(self.keys()))
            ))

    def _post_process(self, key, val):
        post_processor = self.post_processors.get(key)
        if not post_processor:
            return val
        return post_processor(val)

    def _validate(self, key, val):
        validator = self.validators.get(key)
        if not validator:
            return
        if not validator(val):
            raise ParamValidationError('Invalid param: "{}"'.format(key))