import operator
from urllib.parse import urljoin

from liqpay.datastructures import Params
from liqpay.settings import API_URL
from liqpay.utils import generate_request_data


class Form:
    ACTION_URL = urljoin(API_URL, 'checkout/')
    DEFAULT_LANG = 'ru'
    REQUIRED_FIELDS = ['version', 'amount', 'description', 'currency', 'order_id', 'action']

    TEMPLATE = (
        '<form method="post" action="{action}" accept-charset="utf-8">\n'
        '\t{param_inputs}\n'
        '\t<input type="image" src="//static.liqpay.com/buttons/p1{language}.radius.png" name="btn_text"/>\n'
        '</form>'
    )
    INPUT_TEMPLATE = '<input type="hidden" name="{name}" value="{value}"/>'

    def __init__(self, public_key, private_key, lang=None, sandbox=False, params=None):
        self.lang = lang or self.DEFAULT_LANG
        self.public_key = public_key
        self.private_key = private_key
        self.sandbox = sandbox

        self._params = None
        self.params = params

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        if value is None:
            self._params = None
            return
        params = Params(public_key=self.public_key, sandbox=self.sandbox, **value)
        params.require_fields(self.REQUIRED_FIELDS)
        self._params = params

    def get_inputs(self):
        if not self.params:
            raise Exception('Params must be set')
        request_data = generate_request_data(self.private_key, self.params)
        return [
            self.INPUT_TEMPLATE.format(name=k, value=v)
            for k, v in sorted(request_data.items(), key=operator.itemgetter(0))
        ]

    def render(self):
        inputs = self.get_inputs()
        return self.TEMPLATE.format(
            action=self.ACTION_URL,
            language=self.lang,
            param_inputs='\n\t'.join(inputs)
        )
