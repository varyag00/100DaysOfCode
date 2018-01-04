import json
import requests
from pprint import pprint

from exchanges import (
    bittrex,
    bitfinex,
)

BASE_CURRENCY = 'USD'
CRYPTONATOR_URI = 'https://api.cryptonator.com/api/ticker/{base}-{target}'


def convert_currency(base='BTC', target='USD', quantity=1.):
    if base == target:
        return quantity

    try:
        response = requests.get(CRYPTONATOR_URI.format(base=base, target=target)).json()
        result = float(response['ticker']['price']) * quantity
    except KeyError:
        raise ValueError(f'{base}-{target} is an invalid trading pair.')
    return result


def calc_portfolio_valuation(portfolio, base_currency='USD'):
    valuation = [
        {
            'valuation': convert_currency(
                base=coin['symbol'],
                target=base_currency,
                quantity=coin['balance'],
            ),
            'base': base_currency,
            **coin,
        } for coin in portfolio
    ]
    valuation += [sum([coin['valuation'] for coin in valuation])]
    return valuation

with open('api_keys.json') as file:
    data = json.load(file)
    bittrex_creds = data['Bittrex']
    bitfinex_creds = data['Bitfinex']

bittrex_portfolio = bittrex.get_balances(bittrex_creds)
bittrex_valuation = calc_portfolio_valuation(
    bittrex_portfolio,
    base_currency=BASE_CURRENCY
)

print(f'Total bittrex portfolio valuation {BASE_CURRENCY} {bittrex_valuation[-1]}')
pprint(bittrex_valuation[:-1])

bitfinex_porfolio = bitfinex.get_balances(bitfinex_creds)
bitfinex_valuation = calc_portfolio_valuation(
    bitfinex_porfolio,
    base_currency=BASE_CURRENCY
)
print(f'Total bitfinex portfolio valuation {BASE_CURRENCY} {bitfinex_valuation[-1]}')
pprint(bitfinex_valuation[:-1])
