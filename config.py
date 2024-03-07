
# "MINT"

MODE = "MINT"

# Перед запуском обязательно укажите полный путь до папки с вашим расширением MagicEdenWallet
EXTENSION_PATH = 'D:\SlonZerion\MagicEdenWallet\MagicEdenWallet_Extension'

# Количество потоков
THREADS_NUM = 2

# Использовать ли прокси
USE_PROXY = False

# Максимальное количество попыток сделать транзакцию
MAX_RETRY = 3


# ### SWAP

# FROM_ASSET_LIST = ["SOL", ] # список токенов, из которых нужно свапать, каждая итерация выбирает рандомный токен из списка

# TO_ASSET_LIST = ['Wrapped Ethereum', 'USDC', 'Tether USD', 'Dai Stablecoin'] # список токенов, в которые нужно свапать, каждая итерация выбирает рандомный токен из списка

# SWAP_SELF_AMOUNT = [0.000005, 0.00001] # ранодмизированная сумма свапа токена из FROM_ASSET_LIST (от меньшего к большему)

# SWAP_COUNT = [350, 500]  # диапазон количества транзакций рандомное

