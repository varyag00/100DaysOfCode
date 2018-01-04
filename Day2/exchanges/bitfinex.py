import requests
import json
import hashlib
import hmac
import time


BITFINEX_API_URL = 'https://api.bitfinex.com/{path}'
BITFINEX_SYMBOL_PRICE_URL = 'https://api.bitfinex.com/v2/tickers?symbols={symbol}'


class Coin:
    def __init__(self, price, balance):
        self.price = price
        self.balance = balance

    @property
    def total(self):
        return self.price * self.balance


def generate_nonce():
    """Bitfinex nonce must be 13 chars long and strictly increasing"""
    return str(int(round(time.time() * 1000)))


def get_price(symbol='BTC', denom='USD', exchange='bitfinex'):

    if exchange.lower() == 'bitfinex':
        fmt_symbol = f't{symbol.upper()}{denom.upper()}'

        response = requests.get(BITFINEX_SYMBOL_PRICE_URL.format(symbol=fmt_symbol)).json()
        # named tuple would be great for this response
        price = requests.get(BITFINEX_SYMBOL_PRICE_URL.format(symbol=fmt_symbol)).json()[0][1]
        return price


def generate_headers(credentials, path, nonce, body):
    """Generates headers for an authenticated API call"""

    sig = '/api/' + path + nonce + body
    sig_hash = hmac.new(
        credentials['secret'].encode('utf-8'),
        sig.encode('utf-8'),
        hashlib.sha384
    ).hexdigest()

    headers = {
        'bfx-nonce': nonce,
        'bfx-apikey': credentials['key'],
        'bfx-signature': sig_hash,
        'content-type': 'application/json'
    }
    return headers


def get_balances(bitfinex_creds):

    nonce = generate_nonce()
    body = json.dumps({

    })
    orders_path = 'v2/auth/r/wallets'

    headers = generate_headers(
        credentials=bitfinex_creds,
        path=orders_path,
        nonce=nonce,
        body=body,
    )

    response = requests.post(
        BITFINEX_API_URL.format(path=orders_path),
        headers=headers,
        data=body,
        verify=True,
    ).json()

    coins = [
        {
            'symbol': coin[1],
            'balance': coin[2],
        } for coin in response
    ]
    return coins

