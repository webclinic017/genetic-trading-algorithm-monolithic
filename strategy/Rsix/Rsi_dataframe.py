import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))
import pandas_ta as ta
import pandas as pd
import numpy as np
from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")
import warnings
warnings.simplefilter('ignore', FutureWarning)

def run(df, TimeFrame, RSI_length, trading=True):

    # create timeframe #
    df['OpenDateTime'] = pd.to_datetime((df['OpenTime']/1000).astype(int), unit='s')

    if TimeFrame <= 60:
        df = df.loc[df["OpenDateTime"].dt.minute % TimeFrame == 0]
        # df["TimeFrame"] = np.select(conditions, [1], default=0)

    if TimeFrame > 60:
        df = df.loc[df["OpenDateTime"].dt.minute == 00] # keep only HOURS xx:00
        df = df.loc[df["OpenDateTime"].dt.hour % (TimeFrame/60) == 0] 
        
    df.reset_index(drop=True, inplace=True)

    df["Close"]  = df["Close"].apply(lambda x: float(x))
    df["High"]   = df["High"].apply(lambda x: float(x))
    df["Low"]    = df["Low"].apply(lambda x: float(x))
    df["Volume"] = df["Volume"].apply(lambda x: float(x))

    df["RSI"] = ta.rsi(df['Close'], length = RSI_length)
    df.to_csv("test.csv")

    # When backtesting drop N/A
    if trading == False:
        df.dropna(inplace = True)

    df = df.reset_index(drop=True)

    return df

#_____________________________________________

if __name__ == "__main__":

    df = pd.read_csv(f"/home/viceversa/Dropbox/bankof3v/static/SAMPLE/kline/kline1m_5days.csv")

    RSI_length = 12
    tf = 240

    df_rsi = run(df, tf, RSI_length, trading=False)

    print(df_rsi)

    # cols = list(df_rsi.columns.values)

    # df_rsi = df_rsi[['Open', 'High', 'Low', 'Close','OpenTime',  'Volume', 'CloseTime', 'QuoteAssetVolume', 'Trades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore', 'RSI']]
    
    # print(df_rsi)

    # import matplotlib.pyplot as plt

    # df_rsi['OpenTime'] = df_rsi['OpenTime']/1000
    # df_rsi['OpenTime'] = pd.to_datetime((df_rsi['OpenTime']/1000).astype(int), unit='s')

    # plt.plot(df_rsi["OpenTime"], df_rsi["RSI"])

    # plt.gcf().autofmt_xdate()
    # plt.show()