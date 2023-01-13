import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_config")
import sqlite3, math, time
from pprint import pprint
import pandas as pd
import pandas_ta as ta
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#==================================================================
# list_symbols

def fetch_qual_symbols(Session):

    connection = sqlite3.connect(f"{outside_dir}/bankof3v.db")

    connection.row_factory = lambda cursor, row: row[0]

    c = connection.cursor()

    sql = f"SELECT Symbol FROM {Session}"
    c.execute(sql)

    list_symbols = c.fetchall()

    return list_symbols

#_______________________________________________________________
# Dataframe

def create_trade_df(Session, Symbol):

    connection = sqlite3.connect(f"{outside_dir}/bankof3v.db")
    c = connection.cursor()

    sql = f"SELECT * FROM {Session} WHERE Symbol = '{Symbol}'"
    c.execute(sql)

    #_______________________________________________________________
    # PARAMS

    params_column_names = list(map(lambda x: x[0], c.description))

    params_data = c.fetchone()

    df_params = pd.DataFrame([params_data], columns=params_column_names)

    Core    = float(df_params.loc[0, 'Core'])
    Trend   = float(df_params.loc[0, 'Trend'])
    TR      = float(df_params.loc[0, 'TR'])
    ATR     = float(df_params.loc[0, 'ATR'])

    max_param = max(Core, Trend, TR, ATR)

    #_______________________________________________________________
    # KLINE

    kline_sample = f"kline_1m_{Symbol}_BINANCE_TESTNET"

    sql = f"SELECT * FROM {kline_sample} ORDER BY rowid DESC LIMIT {max_param}"
    c.execute(sql)

    kline_column_names = list(map(lambda x: x[0], c.description))

    kline = c.fetchall()

    df = pd.DataFrame(kline, columns=kline_column_names)

    df = df.iloc[::-1]

    # #_______________________________________________________________
    # # Indicator DataFrame

    df["Close"]  = df["Close"].apply(lambda x: float(x))
    df["High"]   = df["High"].apply(lambda x: float(x))
    df["Low"]    = df["Low"].apply(lambda x: float(x))
    df["Volume"] = df["Volume"].apply(lambda x: float(x))

    # [step 1] TrueRange = max(arg_TR) - min(arg_TR) 
    df["HIghestRange"] = df["High"].rolling(int(TR/2)).max()
    df["LowestRange"]  = df["Low"].rolling(int(TR/2)).min()

    # [step 2] NATR = Average(TR/Close, input_ATRlength)
    df["NATR"] = ta.natr(df[f"HIghestRange"], df[f"LowestRange"], df["Close"].shift(1), length = ATR)

    # [step 3] core, upper=(core+natr), lower=(core-natr)
    df["Core"] = ta.vwma(df["Close"], df["Volume"], length=Core)
    df["Upper"] = df["Core"] + (df["Core"] * (df["NATR"]*0.01))
    df["Lower"] = df["Core"] - (df["Core"] * (df["NATR"]*0.01))

    # [step 4] Trend Line
    df["Trend"] = ta.vwma(df["Close"], df["Volume"], length=Trend)

    df.dropna(inplace = True)
    df = df.reset_index(drop=True)

    return df



#===========================================================
if __name__ == "__main__":

    Session = "Diviation_Long_2022_1004_0313_Qualify"

    list_symbols = fetch_qual_symbols(Session)

    for Symbol in list_symbols:

        print(Symbol)

        df = create_trade_df(Session, Symbol)
        print(df)

        Upper  = df['Upper'].iloc[-1]
        Lower  = df['Lower'].iloc[-1]
        Core   = df['Core'].iloc[-1]
        Trend  = df['Trend'].iloc[-1]
        Close  = df['Close'].iloc[-1]

        print(f"Close = {Close}")







