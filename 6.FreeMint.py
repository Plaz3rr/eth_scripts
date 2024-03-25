from web3 import Web3
from datetime import datetime, timedelta
import json
import sys
import time
import os
import random

#Установи ГАЗ!!!! 96 строка
#Задержка между транзакциями 93 строка
#Скрипт активирует функцию mint, контракта ZerionDna, фриминт в сети ETH.  
#Отправляет транзы(Type-2) поочередно с рандомной заданной задержкой. Проверяет газ каждые 25сек и отправляет когда падает до заданных пределов
#для его работы создаем файлы mint.txt (для приватников), last_successful_tx6.txt (для записи посл.транзакции - чтобы после остановки скрипта всегда можно было увидеть посл.успешную транзу)



# Настройки
eth_rpc_url = 'https://eth.meowrpc.com'
contract_address = '0x932261f9Fc8DA46C4a22e31B45c4De60623848bF'
private_keys_file_path = 'mint.txt'
web3 = Web3(Web3.HTTPProvider(eth_rpc_url))
assert web3.isConnected(), "Не удалось подключиться к Ethereum RPC"
contract_address = web3.toChecksumAddress(contract_address)

# Загрузка приватных ключей
private_keys = []
with open(private_keys_file_path, 'r') as file:
    private_keys = [line.strip() for line in file]

# ABI контракта (замените на актуальный ABI вашего контракта)
contract_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"contractURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newBaseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newContractURI","type":"string"}],"name":"setContractURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"}]')  # Замените на реальное ABI

# Создание объекта контракта
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Файл для сохранения информации о последней успешной транзакции
last_tx_file = 'last_successful_tx6.txt'

# Функция для чтения последней успешной транзакции из файла
def read_last_successful_tx():
    if os.path.exists(last_tx_file):
        with open(last_tx_file, 'r') as file:
            return file.read()
    return None


# Функция для сохранения последней успешной транзакции в файл
def save_last_successful_tx(tx_info):
    with open(last_tx_file, 'w') as file:
        file.write(tx_info)

#читаем информацию о последней успешной транзакции
last_successful_tx = read_last_successful_tx()

# Функция отправки транзакций
def send_transactions(private_keys, contract, target_gas_price_gwei):
    transaction_counter = 1
    for private_key in private_keys:
        account = web3.eth.account.privateKeyToAccount(private_key)
        nonce = web3.eth.getTransactionCount(account.address)
        
        # Ожидание подходящей стоимости газа(задаём 89стр)
        while True:
            current_gas_price = web3.eth.gasPrice
            if current_gas_price <= web3.toWei(target_gas_price_gwei, 'gwei'):
                break
            print(f"Стоимость газа {Web3.fromWei(current_gas_price, 'gwei')} gwei, ожидаем уменьшения до {target_gas_price_gwei} gwei.")
            time.sleep(25)
        
        tx = {
            'type': '0x2',
            'chainId': web3.eth.chainId,
            'gas': 115849,
            'maxPriorityFeePerGas': web3.toWei(0.1, 'gwei'),
            'maxFeePerGas': web3.toWei(target_gas_price_gwei, 'gwei'),
            'nonce': nonce,
            'to': contract_address,
            'value': 0,
            'data': '0x1249c58b72db8c0b',
        }
        
        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
         # Получить текущее время +3 часа для GMT+3
        local_time = datetime.utcnow() + timedelta(hours=3)
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
        
        
        print(f'\033[92m>>> Успешно {local_time_str} |{transaction_counter}| Адрес: {account.address} | Хеш: {tx_hash.hex()} | Газ: {Web3.fromWei(tx["maxFeePerGas"], "gwei")} gwei\033[0m')
        save_last_successful_tx(f'Адрес: {account.address} | Хеш: {tx_hash.hex()}')
        
        time.sleep(random.randint(420, 520))

try:
    send_transactions(private_keys, contract, 16)
except KeyboardInterrupt:
    print('\033[92m>>>Скрипт остановлен пользователем.\033[0m')
    with open('last_successful_tx6.txt', 'r') as file:
        last_tx = file.read()
    print('\033[92mПоследняя успешная транзакция: {}\033[0m'.format(last_tx))
