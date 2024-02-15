from web3 import Web3
import json
import random
import sys
import time

#Скрипт для отправки ETH из кошельков privatzk.txt через оффиц.мост ZK-ETH. Отправляет транзы с рандомным числом ETH в заданном диапазоне с задержкой 3-8сек. 
#На 13.02.2024 минимальная сумма чтобы не платить за клейм в сети эфира: 0.01ETH

# Соединение с RPC сети ZkSync
zksync_rpc_url = 'https://1rpc.io/zksync2-era'
web3 = Web3(Web3.HTTPProvider(zksync_rpc_url))
assert web3.isConnected()

# Путь к файлу с приватными ключами
private_keys_file_path = 'privatzk.txt'  # Укажите правильный путь к файлу с приватными ключами


private_keys = []
with open(private_keys_file_path, 'r') as file:
    private_keys = [line.strip() for line in file]

# Адрес и ABI контракта
contract_address = Web3.toChecksumAddress('0x000000000000000000000000000000000000800a')
contract_abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_l2Sender","type":"address"},{"indexed":true,"internalType":"address","name":"_l1Receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"Withdrawal","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_l2Sender","type":"address"},{"indexed":true,"internalType":"address","name":"_l1Receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"_amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"_additionalData","type":"bytes"}],"name":"WithdrawalWithMessage","type":"event"},{"inputs":[{"internalType":"uint256","name":"_account","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"transferFromTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_l1Receiver","type":"address"}],"name":"withdraw","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_l1Receiver","type":"address"},{"internalType":"bytes","name":"_additionalData","type":"bytes"}],"name":"withdrawWithMessage","outputs":[],"stateMutability":"payable","type":"function"}]')


contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Функция для автоматизации отправки транзакций
def automate_transactions(private_keys, contract):
    for private_key in private_keys:
        account = web3.eth.account.privateKeyToAccount(private_key)
        address = account.address
        nonce = web3.eth.getTransactionCount(address)

        # Генерация случайного значения ETH для отправки
        value = random.uniform(0.0101, 0.0107)
        value_in_wei = Web3.toWei(value, 'ether')

        # Строим транзакцию 
        tx = {
            'chainId': 324,  # Chain ID для ZkSync
            'gas': 8522207,  # лимит газа
            'gasPrice': web3.eth.gasPrice,
            'nonce': nonce,
            'to': contract_address,
            'value': value_in_wei,
            'data': contract.encodeABI(fn_name='withdraw', args=[address])
        }

        # Подпись и отправка транзакции
        try:
            signed_tx = account.sign_transaction(tx)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            
         # Определение суммы транзакции в эфире для отображения
            value_eth = Web3.fromWei(value_in_wei, 'ether')
            
         # Вывод сообщения об успешной отправке зеленым цветом
            print(f'\033[92m>>> Успешно | {address} | {value_eth}\033[0m')  # \033[92m - начало зеленого цвета, \033[0m - сброс цвета
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            sys.exit("Скрипт остановлен из-за ошибки.")  # Остановка скрипта в случае ошибки


        # Задержка между транзакциями
        time.sleep(random.randint(10, 16))

# Запускаем функцию отправки транзакций
automate_transactions(private_keys, contract)
