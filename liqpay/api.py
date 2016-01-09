import json
from urllib.parse import urljoin

import requests

from liqpay.datastructures import Params
from liqpay.settings import API_URL
from liqpay.utils import generate_request_data, decode_response_data


class Api:
    REQUIRED_FIELDS = ['version']

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def __call__(self, url, params):
        request_url = self._get_request_url(url)
        request_data = self._get_request_data(params)
        response = requests.post(request_url, data=request_data)
        return json.loads(response.text)

    def decode_callback(self, data, signature):
        """
        https://www.liqpay.com/en/doc/callback
        :param data: function result base64.b64encode(json_string)
        :param signature: function result base64.b64encode(hashlib.sha1(private_key + data + private_key))
        """
        return decode_response_data(self.private_key, data, signature)

    def _get_request_url(self, url):
        return urljoin(API_URL, url)

    def _get_request_data(self, params):
        params = Params(public_key=self.public_key, **params)
        params.require_fields(self.REQUIRED_FIELDS)
        return generate_request_data(self.private_key, params)
