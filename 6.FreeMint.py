from web3 import Web3
import json
import random
import sys
import time
import os

#Скрипт активирует функцию mint, контракта ZerionDna, фриминт в сети ETH.  
#Отправляет транзы поочередно с рандомной заданной задержкой. Проверяет газ(75строка) каждые 10сек и отправляет когда падает до заданных пределов
#для его работы создаем файлы mint.txt (для приватников), last_successful_tx6.txt (для записи посл.транзакции - чтобы после остановки скрипта всегда можно было увидеть посл.успешную транзу)

# Информация для подключения к Ethereum через RPC и данные контракта
eth_rpc_url = 'https://eth.meowrpc.com'
contract_address = '0x932261f9Fc8DA46C4a22e31B45c4De60623848bF'
private_keys_file_path = 'mint.txt'

# Создаем соединение с Ethereum RPC
web3 = Web3(Web3.HTTPProvider(eth_rpc_url))
assert web3.isConnected()

# Чтение приватных ключей из файла
private_keys = []
with open(private_keys_file_path, 'r') as file:
    private_keys = [line.strip() for line in file]

# ABI контракта 
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

# Функция для автоматизации отправки транзакций
def automate_transactions(private_keys, contract):
    global last_successful_tx  # Используем глобальную переменную для хранения данных о последней успешной транзакции

    for private_key in private_keys:
        account = web3.eth.account.privateKeyToAccount(private_key)
        nonce = web3.eth.getTransactionCount(account.address, 'pending')

       
        try:
            # Строим транзакцию
            tx = {
                'chainId': web3.eth.chainId,
                'gas': 115849,  # Заданный лимит газа
                'gasPrice': web3.eth.gasPrice,
                'nonce': nonce,
                'to': contract_address,
                'value': 0,  # Нет отправки эфира
                'data': '0x1249c58b72db8c0b'  # вызов функции mint
            }

            while True:
                gas_price = web3.eth.gasPrice  # Получаем текущую стоимость газа
                if gas_price <= Web3.toWei(15, 'gwei'):
                    break
                print(f"Текущая стоимость газа {Web3.fromWei(gas_price, 'gwei')} gwei, ожидание уменьшения.")
                time.sleep(10)  # Подождите 10 секунд перед следующей проверкой

            # Подпись и отправка транзакции
            signed_tx = account.signTransaction(tx)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            last_successful_tx = f'>>> Успешно | Адрес: {account.address} | Хеш: {tx_hash.hex()}'
            print('\033[92m' + last_successful_tx + '\033[0m')
            save_last_successful_tx(last_successful_tx)

            time.sleep(random.uniform(10, 20))

        except KeyboardInterrupt:
            if last_successful_tx:
                print('\033[92m' + ">>>Скрипт остановлен. Последняя успешная транзакция:" + '\033[0m')
                print('\033[92m' + last_successful_tx + '\033[0m')
            else:
                print('\033[92m' + ">>>Скрипт остановлен. Нет данных о последней успешной транзакции." + '\033[0m')
            sys.exit()


       
# Запускаем функцию отправки транзакций
automate_transactions(private_keys, contract)
