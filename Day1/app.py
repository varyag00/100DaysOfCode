import os
import json
import time
from flask import (
    Flask,
    redirect,
    request,
)
import requests

DEBUG = os.getenv('DEBUG', True)
CRYPTONATOR_URI = 'https://api.cryptonator.com/api/ticker/{base}-{target}'

app = Flask(__name__)


def convert_currency(base='BTC', target='USD', value=1.):
    try:
        response = requests.get(CRYPTONATOR_URI.format(base=base, target=target)).json()
        result = float(response['ticker']['price']) * value
    except KeyError:
        raise ValueError(f'{base}-{target} is an invalid trading pair.')
    return result


@app.route('/')
def index():
    return redirect('/convert')


@app.route('/convert')
def convert():
    base = request.args.get('base').upper()
    target = request.args.get('target').upper()
    value = float(request.args.get('value'))

    try:
        result = convert_currency(base, target, value)
    except ValueError as e:
        response = json.dumps({
            'status': 400,
            'message': str(e),
        })
        return response

    response = json.dumps({
        'base': base,
        'target': target,
        'base_value': value,
        'result': result,
        'timestamp': int(time.time())
    })

    return response

if __name__ == '__main__':
    app.run(debug=DEBUG)
