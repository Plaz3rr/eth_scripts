from web3 import Web3
import time

#Проверь ГАЗ! 22 строка

#Скрипт отправляет максимально возможное количество ETH с кошельков senders.txt на кошельки(напр. суббакаунты) receivers.txt
#Выжидает нужный газ и отправляет, в случае ошибки через 60сек повторяет всё заново с кошелька на котором остановился

# Подключение к Ethereum сети
infura_url = "https://eth.meowrpc.com"
web3 = Web3(Web3.HTTPProvider(infura_url))
assert web3.isConnected()

# Функция для считывания приватных ключей и адресов получателей
def read_private_keys_and_receivers(private_keys_file, receivers_file):
    with open(private_keys_file, 'r') as pk_file:
        private_keys = [line.strip() for line in pk_file.readlines()]
    with open(receivers_file, 'r') as rcv_file:
        receivers = [line.strip() for line in rcv_file.readlines()]
    return private_keys, receivers

def send_max_eth_if_gas_is_low(private_key, receiver, max_gas_price_gwei=31):
    account = web3.eth.account.privateKeyToAccount(private_key)

    while True:
        gas_price = web3.eth.gasPrice
        balance = web3.eth.getBalance(account.address)
        gas_limit = 21000  # Стандартный лимит газа для транзакции ETH
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
            'chainId': 1,  # Для основной сети Ethereum
            'nonce': web3.eth.getTransactionCount(account.address),
            'to': receiver,
            'value': amount_to_send,
            'gas': gas_limit,
            'gasPrice': gas_price
        }

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"\033[92m>>>От {account.address} >>> {web3.fromWei(amount_to_send, 'ether')}ETH на {receiver}, хеш: {web3.toHex(tx_hash)}\033[0m")
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
    # Выводим сообщение о остановке скрипта зелёным цветом
    print('\033[92m>>>Скрипт остановлен пользователем.\033[0m')
