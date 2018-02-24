import json
from collections import MutableMapping

from liqpay.exceptions import ParamValidationError, ParamRequired
from liqpay.constants import SUPPORTED_CURRENCIES, SUPPORTED_LANGUAGES


def _val_not_empty_validator(val):
    return bool(val)


class Params(MutableMapping):
    validators = {
        'public_key': _val_not_empty_validator,
        'amount': lambda x: float(x) > 0,
        'description': _val_not_empty_validator,
        'currency': lambda x: x in SUPPORTED_CURRENCIES,
        'language': lambda x: x in SUPPORTED_LANGUAGES,
    }
    post_processors = {
        'sandbox': lambda x: int(bool(x))
    }

    def __init__(self, *args, **kwargs):
        self._store = {}
        self.update(dict(*args, **kwargs))

    def require_fields(self, fields):
        if not set(fields).issubset(self.keys()):
            raise ParamRequired("Required param(s) not found: '{}'".format(
                ', '.join(set(fields) - self.keys())
            ))

    def to_json(self):
        return json.dumps(self._store, sort_keys=True, ensure_ascii=False)

    def _post_process(self, key, val):
        post_processor = self.post_processors.get(key)
        return post_processor(val) if callable(post_processor) else val

    def _validate_field(self, field, val):
        validator = self.validators.get(field)
        if callable(validator) and not validator(val):
            raise ParamValidationError("Invalid param: '{}'".format(field))

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._validate_field(key, value)
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
