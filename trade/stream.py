import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
import kline
import sqlite3, json, websocket, logging
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

#_____________________________________________________________

def run(Session, ExchangeID, CandleTimeFrame, list_symbols):

    connection = sqlite3.connect(f"{outside_dir}/bankof3v.db")
    c = connection.cursor()


    def on_error(ws, error):
        print(error) 

    def on_message(ws, message):

        # システムをアップデートした際、データベースが消えないよう、プロジェクトの外（並列）にデータベースを作成する
        con = sqlite3.connect(f"{outside_dir}/bankof3v.db")
        cur = con.cursor()

        stream_data             = json.loads(message)
        data                    = stream_data["data"]
        StreamSymbol            = str(data['s'])
        candle                  = data['k']
        #Tick                    = float(candle['c'])
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
                        str(StreamSymbol),\
                        ) ]

        # log.info(kline_stream)

        if is_candle_closed == True:
            try:
                Table_Name = kline.tableName(Session, StreamSymbol, ExchangeID, CandleTimeFrame)
                cur.executemany(f"INSERT INTO {Table_Name} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", kline_stream)
                con.commit()
                log.info(f"Fetched {StreamSymbol}")

            except Exception as e:
                logging.info(f"{e}")

    #---------------------------------------------------------------------------------------------------
    # List Up All The Symbols

    # Prefix Stream EndPoint (Not stream.binance  USE -> fstream.binance for FUTURES)
    Sockets_li = ["wss://fstream.binance.com/stream?streams=",]

    for Symbol in list_symbols:
        
        Symbol = Symbol.lower()
        CandleTimeFrame = "1m"

        data = f'{Symbol}@kline_{CandleTimeFrame}/'
        Sockets_li.append(data)

    # List to String
    SOCKET = ''.join(Sockets_li)
    # Remove "/" at last
    SOCKET = SOCKET[:-1]

    # Let's Stream #
    ws = websocket.WebSocketApp(SOCKET, on_message=on_message, on_error=on_error)
    ws.run_forever()

#_________________________________________________________________________________________

if __name__ == "__main__": 

    from trade import setup

    SessionInfo = setup.run()

    Session         = SessionInfo[2]
    ExchangeID      = SessionInfo[7]
    CandleTimeFrame = SessionInfo[8]
    ExchangeClient  = SessionInfo[9]
    
    list_symbols = ["BTCUSDT", "ETHUSDT"]

    run(Session, ExchangeID, CandleTimeFrame, list_symbols)