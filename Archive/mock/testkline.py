from binance.enums import HistoricalKlinesType
from binance import Client
from pprint import pprint
import time

# Binance #
# binance_api_key         = "TrPEm3uVlRW8Vz8dxtOajM8YWLK7qrXH4T6vX3IaWB6HbGe36upDP4WLZmtglS5b"
# binance_api_secret      = "BvwM01hry9asdWXZZSX6dogi3SwxlImlHzLxQ5zxU3xbb2iplhbIQi34IOlzba3J"

test_binance_api_key    = "d1e2770df3b64f0663c292bea424fa91fb4c07bcde476c319d35f2fe01059675"
test_binance_api_secret = "14bf9fe1a0a3e3674bf61a3cf9181567f205c2c50e7ed859fc16e3702cf6ffa0"

CLIENT = Client(test_binance_api_key, test_binance_api_secret,  {"timeout": 99999}, testnet=True)
CLIENT_KLINE = Client(test_binance_api_key, test_binance_api_secret,  {"timeout": 99999}, testnet=True)

used_weight_1m = int(CLIENT_KLINE.response.headers['x-mbx-used-weight-1m'])

print(used_weight_1m)

# info = client.get_exchange_info()
# info["rateLimits"]

symbol_list = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]

for Symbol in symbol_list:

    print(Symbol)

    while True:

        try:

            head = CLIENT_KLINE.response.headers
            used_weight_1m = int(head['x-mbx-used-weight-1m'])

            s = time.time()

            hist = CLIENT_KLINE.get_historical_klines(Symbol, Client.KLINE_INTERVAL_1MINUTE, "60 day ago UTC", klines_type=HistoricalKlinesType.FUTURES)

            print(hist[0])

            head = CLIENT_KLINE.response.headers
            used_weight_1m = int(head['x-mbx-used-weight-1m'])
            
            elpse = time.time() - s 

            print(f"Request weight is -> {used_weight_1m} (1m), {round(elpse,1)} sec")

            time.sleep(1)

            break

        except Exception as e:

            head = CLIENT_KLINE.response.headers
            used_weight_1m = int(head['x-mbx-used-weight-1m'])
            
            elpse = time.time() - s 

            print(f"Too much request weight? reason {e}. waiting...-> {used_weight_1m} (1m), waiting {round(elpse,1)} sec")

            time.sleep(10)