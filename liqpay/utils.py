import base64
import hashlib
import json
from collections import MutableMapping

from liqpay.datastructures import Params
from liqpay.exceptions import SignatureMismatch


def encode_data(params):
    if not isinstance(params, Params):
        params = Params(params)
    return base64.b64encode(params.to_json().encode('utf-8')).decode()


def generate_signature(private_key, data):
    if isinstance(data, MutableMapping):
        data = encode_data(data)
    signature = private_key + data + private_key
    return base64.b64encode(hashlib.sha1(signature.encode('utf-8')).digest()).decode()


def generate_request_data(private_key, params: Params):
    data = encode_data(params)
    return dict(
        data=data,
        signature=generate_signature(private_key, data)
    )


def decode_response_data(private_key, raw_data, signature):
    json_data = base64.b64decode(raw_data.encode('utf-8')).decode()
    data = json.loads(json_data)
    if signature != generate_signature(private_key, raw_data):
        raise SignatureMismatch
    return data
