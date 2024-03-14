from web3 import Web3
import time
import ccxt
from termcolor import cprint
import random
import json
from decimal import Decimal
import requests
from datetime import datetime
from collections import Counter

#119 строка настрой нужную функцию для отображения инфы по кошелькам из wallets.txt  


# RPC и контракт Скролл оригин НФТ
rpc_url = "https://1rpc.io/scroll"  # Замени это на актуальный RPC endpoint сети Scroll
contract_address = "0x74670A3998d9d6622E32D0847fF5977c37E0eC91"
file_path = "wallets.txt"  # Путь к файлу со списком кошельков

# Подключение к сети
web3 = Web3(Web3.HTTPProvider(rpc_url))

# ABI контракта
contract_abi = json.loads('[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"bytes32","name":"_root","type":"bytes32"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ERC721EnumerableForbiddenBatchMint","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721IncorrectOwner","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721InsufficientApproval","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC721InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"}],"name":"ERC721InvalidOperator","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721InvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC721InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC721InvalidSender","type":"error"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721NonexistentToken","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"ERC721OutOfBoundsIndex","type":"error"},{"inputs":[],"name":"ErrorAlreadyMinted","type":"error"},{"inputs":[],"name":"ErrorCallerIsNotDeployer","type":"error"},{"inputs":[],"name":"ErrorInvalidProof","type":"error"},{"inputs":[],"name":"ErrorTransferIsForbidden","type":"error"},{"inputs":[],"name":"ReentrancyGuardReentrantCall","type":"error"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"StringsInsufficientHexLength","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"metadata","outputs":[{"internalType":"address","name":"deployer","type":"address"},{"internalType":"address","name":"firstDeployedContract","type":"address"},{"internalType":"address","name":"bestDeployedContract","type":"address"},{"internalType":"uint256","name":"rarityData","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"},{"components":[{"internalType":"address","name":"deployer","type":"address"},{"internalType":"address","name":"firstDeployedContract","type":"address"},{"internalType":"address","name":"bestDeployedContract","type":"address"},{"internalType":"uint256","name":"rarityData","type":"uint256"}],"internalType":"struct ScrollOriginsNFT.Metadata","name":"meta","type":"tuple"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"mintData","outputs":[{"internalType":"uint64","name":"mintAt","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"minted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"root","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}]')  # Вставь сюда ABI контракта

# Инициализация контракта для нфт чекера
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

ETHERSCAN_API_KEY = 'вставь свой'
ETHERSCAN_API_URL = 'https://api.scrollscan.com/api'

def get_transaction_history(wallet_address):
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet_address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':  # Успех
            return data['result']
        else:
            print('Ошибка получения данных:', data['message'])
    else:
        print('Ошибка запроса:', response.status_code)
    return []

def calculate_unique_periods(transactions):
    dates = [datetime.utcfromtimestamp(int(tx['timeStamp'])).date() for tx in transactions]
    months = Counter([date.strftime("%Y-%m") for date in dates])
    weeks = Counter([date.strftime("%Y-%W") for date in dates])
    days = Counter([date.strftime("%Y-%m-%d") for date in dates])

    unique_months = len(months)
    unique_weeks = len(weeks)
    unique_days = len(days)
    last_month = max(months, default="Нет данных")  # Получаем последний месяц

    return unique_months, unique_weeks, unique_days, last_month
    
def is_contract(address):
    address = web3.toChecksumAddress(address)
    code = web3.eth.getCode(address)
    return code.hex() != '0x'

def calculate_unique_contracts(wallet_address):
    transactions = get_transaction_history(wallet_address)
    unique_contracts = set()

    for tx in transactions:
        # Проверяем, является ли адресат контрактом
        if tx['to']:
            to_address = web3.toChecksumAddress(tx['to'])
            if is_contract(to_address):
                unique_contracts.add(to_address)
        
        # Определение транзакций создания контракта
        
        elif not tx['to'] and tx['input'] and len(tx['input']) > 2:  # '0x' - пустой input
            
            unique_contracts.add(tx['hash'])

    return len(unique_contracts)


# Чтение адресов из файла и проверка активности
def calculate_activity(wallet_address):
    transactions = get_transaction_history(wallet_address)
    if not transactions:
        return "нет данных об активности"
    
    unique_months, unique_weeks, unique_days, last_month = calculate_unique_periods(transactions)
    return f"{unique_months}m/{unique_weeks}w/{unique_days}d, последний месяц: {last_month}"
    
# Функция для проверки наличия NFT у кошелька
def check_nft_ownership(wallet_address):
    balance = contract.functions.balanceOf(wallet_address).call()
    return balance

# Функция для проверки количества исходящих транзакций
def check_outgoing_transactions(wallet_address):
    transaction_count = web3.eth.getTransactionCount(wallet_address)
    return transaction_count

# Словарь функций проверки
check_functions = {
    'nft': check_nft_ownership,
    'transactions': check_outgoing_transactions,
    'activity': calculate_activity,
    'unique_contracts': calculate_unique_contracts
    # Добавьте новые функции проверки сюда
}

# Выбор функции для проверки
#current_check =  'nft' 
#current_check =  'transactions'
current_check = 'activity'
#current_check = 'unique_contracts'

# Функция для выполнения выбранной проверки
def perform_check_and_log(check_key, wallet_address, index):
    if check_key in check_functions:
        result = check_functions[check_key](wallet_address)
        
        # Логирование результатов в зависимости от типа проверки
        if check_key == 'unique_contracts':
            print(f"{index}.Кошелек {wallet_address} взаимодействовал с {result} уникальными контрактами.")
        elif check_key == 'nft':
            if result > 0:
                print(f"{index}. Кошелек {wallet_address} владеет {result} NFT.")
            else:
                cprint(f"{index}. Кошелек {wallet_address} не владеет NFT.", 'red')
        elif check_key == 'transactions':
            print(f"{index}. Кошелек {wallet_address} имеет {result} исходящих транзакций.")
        elif check_key == 'activity':
            print(f"{index}. Кошелек {wallet_address} активен {result}")
    else:
        print(f"Проверка '{check_key}' не найдена.")

# Чтение адресов из файла и проверка
with open(file_path, 'r') as file:
    for index, line in enumerate(file, start=1):
        wallet_address = line.strip()
        perform_check_and_log(current_check, wallet_address, index)
