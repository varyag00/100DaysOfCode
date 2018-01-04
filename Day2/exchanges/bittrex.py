import requests
import json
import hashlib
import hmac
import uuid

BITTREX_API_URL = 'https://bittrex.com/api/v1.1/account/getbalances?apikey={apikey}&nonce={nonce}'


def generate_nonce(length=8):
    return str(uuid.uuid4())[0:length]


def calc_hash(uri, secret):
    hash = hmac.new(secret.encode('utf-8'), uri.encode('utf-8'), hashlib.sha512).hexdigest()
    return hash


def sanitize_symbol(symbol):
    if symbol == 'BCC':
        return 'BCH'
    if symbol == 'USDT':
        return 'USD'
    return symbol


def get_balances(bittrex_creds):
    bittrex_uri = BITTREX_API_URL.format(
        apikey=bittrex_creds['key'],
        nonce=generate_nonce(8),
    )
    hash = calc_hash(bittrex_uri, bittrex_creds['secret'])

    bittrex_currencies = requests.get(
        url=bittrex_uri,
        headers={
            'apisign': hash
        }
    ).json()['result']
    filtered_currencies = [
        {
            'symbol': sanitize_symbol(currency['Currency']),
            'balance': currency['Balance'],
        } for currency in bittrex_currencies if currency['Balance'] > 0
    ]

    return filtered_currencies

