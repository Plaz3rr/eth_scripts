import time
import ccxt
from termcolor import cprint
from web3 import Web3
import random
from decimal import Decimal, ROUND_DOWN

#скрипт выводит эфир с банана на кошельки из wallets.txt пополняя их на такую сумму, чтобы итоговый баланс кошельков был в пределах заданной суммы стр 76
#Проверь РПЦ!!! 51 и ниже
#28 строка - мин сумма вывода на банане, стр 76 - минимум нужной суммы
#78 строка - сумма комиссии банана
def check_balance(address, number, web3):
    try:
        balance = web3.eth.get_balance(web3.toChecksumAddress(address))
        humanReadable = web3.fromWei(balance, 'ether')
        cprint(f'{number}. {address} : {humanReadable}', 'white')
    except Exception as error:
        cprint(f'{number}. {address} = {error}', 'red')

def binance_withdraw(number, address, amount_to_withdrawal, symbolWithdraw, network, API_KEY, API_SECRET):
    account_binance = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    })
    min_withdrawal_amount_eth = Decimal('0.002')  # Минимальная сумма для вывода на Binance
    if amount_to_withdrawal < min_withdrawal_amount_eth:
        amount_to_withdrawal = min_withdrawal_amount_eth
    try:
        account_binance.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            tag=None, 
            params={
                "network": network
            }
        )
        cprint(f">>> Выполняется операция номер [{number}]:", "green")
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
    RPC = 'https://mainnet.era.zksync.io'
    web3 = Web3(Web3.HTTPProvider(RPC))

    API_KEY = "...."  # Вставьте ваш API Key
    API_SECRET = "...."  # Вставьте ваш Secret Key

    cprint('\a\n/// Начинаем проверку балансов...', 'white')
    number = 0
    for wallet in wallets_list:
        address = web3.toChecksumAddress(wallet)
        number += 1
        check_balance(address, number, web3)  # Проверяем баланс ETH

    
    cprint('\a\n/// Начинаем вывод...', 'white')
    desired_min_balance_eth = 0.0114  # Минимальный желаемый баланс в ETH
    desired_max_balance_eth = 0.0118  # Максимальный желаемый баланс в ETH
    binance_withdrawal_fee = Decimal('0.00015')
    number = 1
    for wallet in wallets_list:
        address = web3.toChecksumAddress(wallet)
        current_balance = web3.eth.get_balance(address)
        current_balance_eth = Decimal(web3.fromWei(current_balance, 'ether'))
    
        
        if current_balance_eth < desired_min_balance_eth:
           # Если текущий баланс меньше минимального желаемого баланса
           
           desired_balance_eth = Decimal(random.uniform(desired_min_balance_eth, desired_max_balance_eth))
        # Рассчитываем необходимую сумму для "вывода" (пополнения)
           amount_to_add = (desired_balance_eth + binance_withdrawal_fee) - current_balance_eth
           amount_to_add = amount_to_add.quantize(Decimal('0.00001'), rounding=ROUND_DOWN)
        # Вызываем функцию для "вывода" средств
           binance_withdraw(number, address, float(amount_to_add), symbolWithdraw, network, API_KEY, API_SECRET)
           cprint(f"Пополняем {address} на {amount_to_add} ETH для достижения желаемого баланса.", "green")
           number += 1
        else:
           cprint(f"Пропуск {address}. Текущий баланс уже соответствует желаемому.", "yellow")
        

        
        time.sleep(random.randint(12, 30))
