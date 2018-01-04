from bs4 import BeautifulSoup
import requests

ETHERSCAN_URI = 'https://etherscan.io/address/{addr}'


def get_balance(addr):
    """Get the balance at a given ethereum address"""
    etherscan_page = requests.get(ETHERSCAN_URI.format(addr=addr)).text
    bs = BeautifulSoup(etherscan_page, 'html.parser')

    # NB: address balance _appears_ to be immediately after the td containing "ETH Balance:"
    td_list = bs.find_all('td')
    for index, td in enumerate(td_list):
        if 'ETH Balance:' in td.text:
            return float(td_list[index+1].text.split(' ')[0])
    else:
        raise Exception(f'An unexpected error occurred while analyzing wallet {addr}')

