
from dotenv import load_dotenv
load_dotenv()

import os
binance_api_key = os.getenv('binance_api_key')
binance_api_secret = os.getenv('binance_api_secret')

test_binance_api_key = os.getenv('test_binance_api_key')
test_binance_api_secret = os.getenv('test_binance_api_secret')

AWS_access_key_id = os.getenv('AWS_access_key_id')
AWS_secret_access_key = os.getenv('AWS_secret_access_key')
AWS_region = os.getenv('AWS_region')
AWS_instance = os.getenv('AWS_instance')


