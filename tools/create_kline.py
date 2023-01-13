import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
from config import pw
from binance.client import Client
from binance.enums import HistoricalKlinesType
import numpy as np
import sqlite3, math, time, logging, multiprocessing, os
import ast
import pandas as pd
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

time_start = time.time()
##################

ExchangeClient = Client(pw.binance_api_key, pw.binance_api_secret)

days = 365

kline_data = ExchangeClient.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE,\
    f"{days} day ago UTC", klines_type=HistoricalKlinesType.FUTURES)

col = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume',\
        'Trades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore']

df_kline = pd.DataFrame(kline_data, columns = col)

directry = "static/SAMPLE/kline/"
os.makedirs(directry, exist_ok=True)

df_kline.to_csv(f"{directry}kline1m_{days}days.csv", index=False)


##################
time_elapse = round((time.time() - time_start)/60,2)

print(f"\ntotal bars -> {len(df_kline)}")
print(f"elapse{time_elapse} min\n")
