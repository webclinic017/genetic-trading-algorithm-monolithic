import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_config")

import os, time, sys, logging, time, schedule, sqlite3, json, websocket
from config import binance_data
from strategy import DeviL, DeviS

from timeout_decorator import timeout

import rich
from rich import pretty, print
from rich.console import Console
import time
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

# --------------------------------------------------------------------------------------------------------

# day_sec = 1440*60

# @timeout(day_sec)
def stream(list_symbols):

    exchangeName = "BINANCE_TESTNET"

    def on_error(ws, error):
        print(error) 

    def on_message(ws, message):

        # システムをアップデートした際、データベースが消えないよう、プロジェクトの外（並列）にデータベースを作成する
        con = sqlite3.connect(f"{outside_dir}/bankof3v.db")
        cur = con.cursor()

        stream_data             = json.loads(message)
        data                    = stream_data["data"]
        symbol                  = str(data['s'])
        candle                  = data['k']
        Tick                    = float(candle['c'])
        OpenTime                = candle['t']
        Open                    = candle['o']
        High                    = candle['h']
        Low                     = candle['l']
        Close                   = candle['c']
        Volume                  = candle['v']
        CloseTime               = candle['T']
        QuoteAssetVolume        = candle['q']
        Trades                  = candle['n']
        TakerBuyBaseAssetVolume = candle['V']
        TakerBuyQuoteAssetVolume= candle['Q']
        is_candle_closed        = candle['x']

        kline_stream = [ ( OpenTime,\
                        Open,\
                        High,\
                        Low,\
                        Close,\
                        Volume,\
                        CloseTime,\
                        QuoteAssetVolume,\
                        Trades,\
                        TakerBuyBaseAssetVolume,\
                        TakerBuyQuoteAssetVolume,\
                        bool(is_candle_closed),\
                        str(symbol),\
                        ) ]

        # log.info(kline_stream)

        Table_Name = f"kline_1m_{symbol}_{exchangeName}"

        if is_candle_closed == True:
            try:
                cur.executemany(f"INSERT INTO {Table_Name} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", kline_stream)
                con.commit()
                log.info(f"Fetched {symbol}")

            except Exception as e:
                logging.info(f"{e}")

    #---------------------------------------------------------------------------------------------------

    # List Up All The Symbols

    # Prefix Stream EndPoint (Not stream.binance  USE -> fstream.binance for FUTURES)
    Sockets_li = ["wss://fstream.binance.com/stream?streams=",]

    # Create Strings
    for index, Symbol in enumerate(list_symbols):
        
        Symbol = Symbol.lower()
        tf = "1m"

        data = f'{Symbol}@kline_{tf}/'
        Sockets_li.append(data)

    # List to String
    SOCKET = ''.join(Sockets_li)
    # Remove "/" at last
    SOCKET = SOCKET[:-1]

    # Let's Stream #
    ws = websocket.WebSocketApp(SOCKET, on_message=on_message, on_error=on_error)
    ws.run_forever()


# TEST #
if __name__ == "__main__":
    list_symbols = ["BTCUSDT"]

    stream(list_symbols)




