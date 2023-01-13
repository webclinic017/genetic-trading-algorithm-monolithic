import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))
import pandas_ta as ta

from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

import warnings
warnings.simplefilter('ignore', FutureWarning)

"""
-------------------------------  DATAFRAME ---------------------------------
"""
def run(df, ATR, CORE, TR, TREND, trading=True):
    
    df["Close"]  = df["Close"].apply(lambda x: float(x))
    df["High"]   = df["High"].apply(lambda x: float(x))
    df["Low"]    = df["Low"].apply(lambda x: float(x))
    df["Volume"] = df["Volume"].apply(lambda x: float(x))

    # [step 1] TrueRange = max(arg_TR) - min(arg_TR) 
    df["HighestRange"] = df["High"].rolling(int(TR/2)).max()
    df["LowestRange"]  = df["Low"].rolling(int(TR/2)).min()

    # [step 2] NATR = Average(TR/Close, input_ATRlength)
    df["NATR"]  = ta.natr(df[f"HighestRange"], df[f"LowestRange"], df["Close"].shift(1), length=ATR)

    # [step 3] core, upper=(core+natr), lower=(core-natr)
    df["CORE"]  = ta.vwma(df["Close"], df["Volume"], length=CORE)
    df["Upper"] = df["CORE"] + (df["CORE"] * (df["NATR"]*0.01))
    df["Lower"] = df["CORE"] - (df["CORE"] * (df["NATR"]*0.01))

    # [step 4] TREND Line
    df["TREND"] = ta.vwma(df["Close"], df["Volume"], length=TREND)

    # When backtesting drop N/A
    if trading == False:
        df.dropna(inplace = True)

    df = df.reset_index(drop=True)

    return df