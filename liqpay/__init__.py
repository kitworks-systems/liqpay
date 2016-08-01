"""
LiqPay Python SDK
~~~~~~~~~~~~~~~~~
supports Python 3.x version
requires requests module
"""

__title__ = 'LiqPay Python SDK'
__version__ = '1.0'


__all__ = ['LiqPay']


from liqpay.api import Api
from liqpay.forms import Form


class LiqPay:
    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key
        self.api = Api(self._public_key, self._private_key)

    def get_form(self, sandbox=False, params=None):
        return Form(self._public_key, self._private_key, sandbox, params)
