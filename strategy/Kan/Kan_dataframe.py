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


def run(df, TimeFrame, VWMA_LENGTH, ENTRY_DIV, trading=True):

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

    df["VWMA"] = ta.vwma(df['Close'], df["Volume"], length = VWMA_LENGTH)

    # VWMA_DEVI vwma
    df["VWMA_DEVI"] = df["VWMA"]*((ENTRY_DIV+100)/100)

    # When backtesting drop N/A
    if trading == False:
        df.dropna(inplace = True)

    df = df.reset_index(drop=True)

    return df

#_____________________________________________

if __name__ == "__main__":

    df = pd.read_csv(f"/home/viceversa/Dropbox/bankof3v/static/SAMPLE/kline/kline1m_5days.csv")

    VWMA_LENGTH = 720
    # IF LONG, minus. SHORT is puls.
    ENTRY_DIV = -4 # % ENTRY_DIVERGENCE
    tf = 1

    df = run(df, tf, VWMA_LENGTH, ENTRY_DIV, trading=False)

    print(df)

    cols = list(df.columns.values)

    df = df[['Open', 'High', 'Low', 'Close',
            'OpenTime',  'Volume', 'CloseTime', 'QuoteAssetVolume', 
            'Trades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore', 
            'VWMA', 'VWMA_DEVI']]
    
    print(df)

    import matplotlib.pyplot as plt

    df['OpenTime'] = df['OpenTime']/1000
    df['OpenTime'] = pd.to_datetime((df['OpenTime']/1000).astype(int), unit='s')

    plt.plot(df["OpenTime"], df["Close"])
    plt.plot(df["OpenTime"], df["VWMA"])
    plt.plot(df["OpenTime"], df["VWMA_DEVI"])

    plt.gcf().autofmt_xdate()
    plt.show()