from liqpay.api import Api
from liqpay.forms import Form


__all__ = ['LiqPay']


class LiqPay:
    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key
        self.api = Api(self._public_key, self._private_key)

    def get_form(self, sandbox=False, params=None):
        return Form(self._public_key, self._private_key, sandbox, params)
