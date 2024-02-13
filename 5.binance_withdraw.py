import time
import ccxt
from termcolor import cprint
from web3 import Web3
import random

#Выбери Network и RPC и поставь на вывод любую монету(строка 50) с банана с кошельков из wallets.txt с заданной рандомной задержкой и суммой
#Вставь сюда(64 строка) свои API из аккаунта на банане и добавь в его настройках свой актуальный IP 


def check_balance(address, number, web3):
    try:
        balance = web3.eth.get_balance(web3.toChecksumAddress(address))
        humanReadable = web3.fromWei(balance,'ether')
        cprint(f'{number}. {address} : {humanReadable}', 'white')

    except Exception as error:
        cprint(f'{number}. {address} = {error}', 'red')

def binance_withdraw(address, amount_to_withdrawal, symbolWithdraw, network, API_KEY, API_SECRET):

    account_binance = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    })

    try:
        account_binance.withdraw(
            code = symbolWithdraw,
            amount = amount_to_withdrawal,
            address = address,
            tag = None, 
            params = {
                "network": network
            }
        )
        cprint(f">>> Успешно | {address} | {amount_to_withdrawal}", "green")
    except Exception as error:
        cprint(f">>> Неудачно | {address} | ошибка : {error}", "red")

if __name__ == "__main__":
    
    with open("wallets.txt", "r") as f:
        wallets_list = [row.strip() for row in f]

    symbolWithdraw = 'ETH'
    network = 'ZKSYNCERA'
    # network = 'Arbitrum'
    # network = 'ETH'

    # RPC = 'https://mainnet.optimism.io'
    # RPC = 'https://bsc-dataseed.binance.org'
    # RPC = 'https://polygon-rpc.com'
    # RPC = 'https://arb1.arbitrum.io/rpc'
    # RPC = 'https://rpc.ankr.com/eth'
    RPC = 'https://1rpc.io/zksync2-era'
    web3 = Web3(Web3.HTTPProvider(RPC))

    # api_keys of binance
    API_KEY = "ВСТАВЬ СВОЙ"
    API_SECRET = "ВСТАВЬ СВОЙ"

    cprint('\a\n/// start check balance...', 'white')
    number = 0
    for wallet in wallets_list:
        address = web3.toChecksumAddress(wallet)
        number = number + 1
        check_balance(address, number, web3) # проверяет баланс ETH

    cprint('\a\n/// start withdrawing...', 'white')
    for wallet in wallets_list:
        address = web3.toChecksumAddress(wallet)
        amount_to_withdrawal = round(random.uniform(0.01026, 0.01027), 6) # amount from ... to ...
        binance_withdraw(address, amount_to_withdrawal, symbolWithdraw, network, API_KEY, API_SECRET)
        time.sleep(random.randint(10, 30))
