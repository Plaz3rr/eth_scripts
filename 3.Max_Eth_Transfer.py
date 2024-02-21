from web3 import Web3
import time
import os
import sys

#Настройки:
# 14 строка - RPC
# 62 строка - gazlimit
# 83 строка - chain ID

#Скрипт отправляет максимально возможное количество ETH с кошельков senders.txt на кошельки(напр. суббакаунты) receivers.txt
#Выжидает нужный газ и отправляет, в случае ошибки через 60сек повторяет всё заново с кошелька на котором остановился

# !Подключение к нужной сети!
infura_url = "https://endpoints.omniatech.io/v1/arbitrum/one/public"
#infura_url = "https://eth.meowrpc.com"
web3 = Web3(Web3.HTTPProvider(infura_url))
assert web3.isConnected()

def read_receivers(receivers_file):
    with open(receivers_file, 'r') as rcv_file:
        receivers = [line.strip().lower() for line in rcv_file.readlines()]  # Приведение адресов к нижнему регистру
    return receivers

# Файл для сохранения информации о последней успешной транзакции
last_tx_file = 'last_successful_tx3.txt'

# Функция для чтения последней успешной транзакции из файла
def read_last_successful_tx():
    if os.path.exists(last_tx_file):
        with open(last_tx_file, 'r') as file:
            return file.read()
    return None


# Функция для сохранения последней успешной транзакции в файл
def save_last_successful_tx(account_address, receiver_address, amount_eth, tx_hash):
    tx_info = f"От {account_address} >>> {amount_eth}ETH на {receiver_address}, хеш: {tx_hash}"
    with open(last_tx_file, 'w') as file:
        file.write(tx_info)


#читаем информацию о последней успешной транзакции
last_successful_tx = read_last_successful_tx()

# Функция для считывания приватных ключей и адресов получателей
def read_private_keys_and_receivers(private_keys_file, receivers_file):
    with open(private_keys_file, 'r') as pk_file:
        private_keys = [line.strip() for line in pk_file.readlines()]
    with open(receivers_file, 'r') as rcv_file:
        receivers = [line.strip() for line in rcv_file.readlines()]
    return private_keys, receivers

def send_max_eth_if_gas_is_low(private_key, receiver, max_gas_price_gwei=1):
    global last_successful_tx  # Используем глобальную переменную для хранения данных о последней успешной транзакции
    receiver = web3.toChecksumAddress(receiver)
    account = web3.eth.account.privateKeyToAccount(private_key)

    while True:
        gas_price = web3.eth.gasPrice
        balance = web3.eth.getBalance(account.address)
        # gas_limit = 21000  # Стандартный лимит газа для транзакции ETH
        gas_limit = 920000   # в притык должно хватать для ARBITRUM
        gas_cost = gas_price * gas_limit

        # Проверяем, достаточно ли средств на балансе для покрытия стоимости газа
        if balance <= gas_cost:
            print("Недостаточно средств для покрытия стоимости газа. Повторная попытка через минуту...")
            time.sleep(60)
            continue

        # Проверяем стоимость газа
        if gas_price > web3.toWei(max_gas_price_gwei, 'gwei'):
            print(f"Стоимость газа {web3.fromWei(gas_price, 'gwei')} Gwei выше порога {max_gas_price_gwei} Gwei. Ожидание уменьшения стоимости газа...")
            time.sleep(10)
            continue

        # Расчёт максимально возможной суммы для отправки
        amount_to_send = balance - gas_cost

        # Создаем и отправляем транзакцию
        tx = {
            'chainId': 42161,  # Для ARB
            #'chainId': 1, # Для ETH
            'nonce': web3.eth.getTransactionCount(account.address),
            'to': receiver,
            'value': amount_to_send,
            'gas': gas_limit,
            'gasPrice': gas_price
        }

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"\033[92m>>>От {account.address} >>> {web3.fromWei(amount_to_send, 'ether')}ETH на {receiver}, хеш: {web3.toHex(tx_hash)}\033[0m")
        
        # Здесь сохраняем информацию о последней успешной транзакции
        
        amount_eth = web3.fromWei(amount_to_send, 'ether')
        save_last_successful_tx(account.address, receiver, amount_eth, web3.toHex(tx_hash))
        
        break  # Выходим из цикла после успешной отправки

try:
    # Считываем приватные ключи и адреса получателей
    private_keys_file = "senders.txt"
    receivers_file = "receivers.txt"
    private_keys, receivers = read_private_keys_and_receivers(private_keys_file, receivers_file)

    # Перебираем пары отправитель-получатель и отправляем ETH
    for private_key, receiver in zip(private_keys, receivers):
        send_max_eth_if_gas_is_low(private_key, receiver)

except KeyboardInterrupt:
            if last_successful_tx:
                print('\033[92m' + ">>>Скрипт остановлен. Последняя успешная транзакция:" + '\033[0m')
                print('\033[92m' + last_successful_tx + '\033[0m')
            else:
                print('\033[92m' + ">>>Скрипт остановлен. Нет данных о последней успешной транзакции." + '\033[0m')
            sys.exit()
