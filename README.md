Самодельные (GPT) скриптецы

1. Blur_deposit.py - Скрипт отправляет рандомные суммы ETH в заданных пределах, поочередно с рандомной заданной задержкой, на контракт Blur, активируя функцию Deposit. Проверяет газ каждые 10сек и отправляет когда падает до заданных пределов. Для его работы создаем файлы blur_dep.txt (для приватников), last_successful_tx.txt (для записи посл.транзакции - чтобы после остановки скрипта всегда можно было увидеть посл.успешную транзу)
2. ETH_balance_checker.py - проверяем РПЦ и чекаем баланс кошельков из файла wallets.txt в ETH и его стоимость в USDC
3. Max_Eth_Transfer.py - Скрипт отправляет максимально возможное количество ETH с кошельков senders.txt на кошельки(напр. суббакаунты) receivers.txt ...Выжидает нужный газ и отправляет, в случае ошибки через 60сек повторяет всё заново с кошелька на котором остановился. Вычищает кошели под 0
4. Скрипт для отправки ETH из кошельков privatzk.txt через оффиц.мост ZK-ETH(portal.zksync.io). Отправляет транзы с рандомным числом ETH в заданном диапазоне с задержкой 3-8сек. На 13.02.2024 минимальная сумма чтобы не платить за клейм в сети эфира: 0.01ETH
5. binance_withdraw.py - Выбери Network и RPC и поставь на вывод любую монету(строка 50) с банана с кошельков из wallets.txt с заданной рандомной задержкой и суммой. Вставь сюда(64 строка) свои API из аккаунта на банане и добавь в его настройках свой актуальный IP 
