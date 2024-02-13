from web3 import Web3
import json
import random
import sys
import time
import os

#Скрипт отправляет рандомные суммы ETH в заданных пределах, поочередно с рандомной заданной задержкой, на контракт Blur, активируя функцию Deposit. 
#Проверяет газ каждые 10сек и отправляет когда падает до заданных пределов
#для его работы создаем файлы blur_dep.txt (для приватников), last_successful_tx.txt (для записи посл.транзакции - чтобы после остановки скрипта всегда можно было увидеть посл.успешную транзу)

# Информация для подключения к Ethereum через RPC и данные контракта
eth_rpc_url = 'https://eth.meowrpc.com'
contract_address = '0x0000000000A39bb272e79075ade125fd351887Ac'
private_keys_file_path = 'blur_dep.txt'

# Создаем соединение с Ethereum RPC
web3 = Web3(Web3.HTTPProvider(eth_rpc_url))
assert web3.isConnected()

# Чтение приватных ключей из файла
private_keys = []
with open(private_keys_file_path, 'r') as file:
    private_keys = [line.strip() for line in file]

# ABI контракта 
contract_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_logic","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"stateMutability":"payable","type":"receive"}]')  # Замените на реальное ABI

# Создание объекта контракта
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Файл для сохранения информации о последней успешной транзакции
last_tx_file = 'last_successful_tx.txt'

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

        # Генерация случайной суммы ETH для отправки
        value = random.uniform(0.00001, 0.00002)
        value_in_wei = Web3.toWei(value, 'ether')

        try:
            # Строим транзакцию
            tx = {
                'chainId': web3.eth.chainId,
                'gas': 80000,  # Заданный лимит газа
                'gasPrice': web3.eth.gasPrice,
                'nonce': nonce,
                'to': contract_address,
                'value': value_in_wei,
                'data': '0xd0e30db0'  # вызов функции deposit
            }

            while True:
                gas_price = web3.eth.gasPrice  # Получаем текущую стоимость газа
                if gas_price <= Web3.toWei(18, 'gwei'):
                    break
                print(f"Текущая стоимость газа {Web3.fromWei(gas_price, 'gwei')} gwei, ожидание уменьшения.")
                time.sleep(10)  # Подождите 10 секунд перед следующей проверкой

            # Подпись и отправка транзакции
            signed_tx = account.signTransaction(tx)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            # Определение суммы транзакции в эфире для отображения
            value_eth = Web3.fromWei(value_in_wei, 'ether')
            last_successful_tx = f'>>> Успешно | Адрес: {account.address} | Сумма: {value_eth:.6f} ETH | Хеш: {tx_hash.hex()}'
            print('\033[92m' + last_successful_tx + '\033[0m')
            save_last_successful_tx(last_successful_tx)

            time.sleep(random.uniform(5, 10))

        except KeyboardInterrupt:
            if last_successful_tx:
                print('\033[92m' + ">>>Скрипт остановлен. Последняя успешная транзакция:" + '\033[0m')
                print('\033[92m' + last_successful_tx + '\033[0m')
            else:
                print('\033[92m' + ">>>Скрипт остановлен. Нет данных о последней успешной транзакции." + '\033[0m')
            sys.exit()


       
# Запускаем функцию отправки транзакций
automate_transactions(private_keys, contract)
