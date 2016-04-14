import unittest

from liqpay import LiqPay
from liqpay.exceptions import ParamValidationError, SignatureMismatch, ParamRequired
from liqpay.utils import generate_signature, encode_data, decode_response_data


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.private_key = 'privateKey'

    def test_data_encoding(self):
        expected = 'eyJmaWVsZCI6ICJ2YWx1ZSJ9'
        data = dict(field='value')
        encoded = encode_data(data)
        self.assertEqual(expected, encoded)

    def test_signature_generation(self):
        expected = 'cJxZYijbaA+bXqIJIPSV1G0v8DI='

        data = dict(field='value')
        signature = generate_signature(self.private_key, data)
        self.assertEqual(expected, signature)

        data = encode_data(data)
        signature = generate_signature(self.private_key, data)
        self.assertEqual(expected, signature)

    def test_response_decoder(self):
        data = dict(field='value')
        encoded = encode_data(data)
        signature = generate_signature(self.private_key, encoded)

        decoded = decode_response_data(self.private_key, encoded, signature)
        self.assertEqual(data, decoded)
        self.assertRaises(SignatureMismatch, decode_response_data, self.private_key, encoded, 'privateKey2')


class LiqPayTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.liqpay = LiqPay('publicKey', 'privateKey')

    def test_api(self):
        url = 'payment/status'
        params = dict(payment_id=3940)

        self.assertRaises(ParamRequired, self.liqpay.api, url, params)
        params.update(version=3)
        res = self.liqpay.api(url, params)
        self.assertEqual(res['err_code'], 'public_key_not_found')

    def test_form(self):
        params = {
            'amount': '3940',
            'currency': 'UAH',
            'description': 'test',
            'action': 'pay',
            'version': 3,
            'order_id': 1,
        }
        expected_form_out = (
            '<form method="post" action="https://www.liqpay.com/api/checkout/" accept-charset="utf-8">\n'
            '\t<input type="hidden" name="data" value="{data}"/>\n'
            '\t<input type="hidden" name="signature" value="{signature}"/>\n'
            '\t<input type="image" src="//static.liqpay.com/buttons/p1ru.radius.png" name="btn_text"/>\n'
            '</form>'
        ).format(
            data='eyJhY3Rpb24iOiAicGF5IiwgImFtb3VudCI6ICIzOTQwIiwgImN1cnJlbmN5IjogIlVBSCIsICJkZXNjcmlwdGlvbiI6ICJ0ZXN0IiwgIm9yZGVyX2lkIjogMSwgInB1YmxpY19rZXkiOiAicHVibGljS2V5IiwgInNhbmRib3giOiAxLCAidmVyc2lvbiI6IDN9',
            signature='nELNtiwxyaLzvj1hmCrxt78W/qE='
        )
        form = self.liqpay.get_form(sandbox=True, params=params)

        self.assertEqual(form.render(), expected_form_out)

        # test form without required param
        del params['amount']
        with self.assertRaises(ParamRequired):
            form.params = params

        # test params validation
        params['currency'] = 'MXN'  # unsupported currency
        with self.assertRaises(ParamValidationError):
            form.params = params


if __name__ == '__main__':
    unittest.main()
