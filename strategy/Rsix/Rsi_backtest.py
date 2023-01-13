import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))
import Rsi_dataframe, Rsi_logic
from benchmark import module as BT_module
import numpy as np
import joblib as job
import warnings
warnings.simplefilter('ignore', FutureWarning)
warnings.filterwarnings('ignore')

# RSI_length
P1_min,P1_max,P1_cut = 10,30,20
# RSI_ENTRY_LONG
P2_LONG_min,P2_LONG_max,P2_LONG_cut = 20,40,20
# RSI_ENTRY_SHORT
P2_SHORT_min,P2_SHORT_max,P2_SHORT_cut = 60,80,20
# RSI_EXIT_
P3_min,P3_max,P3_cut = 40,60,20
#____________________________________________________________________________________________________________

def run(df_kline, TimeFrame, Strategy, INPUT_RSI_LENGTH, INPUT_RSI_ENTRY, INPUT_RSI_EXIT):

    df = Rsi_dataframe.run(df_kline, TimeFrame, INPUT_RSI_LENGTH,  False)
    side = list(Strategy)[-1] 

    indexLen   = len(df)
    data_OpenTime = df["OpenTime"].tolist()
    data_Close = df["Close"].tolist()
    data_High  = df["High"].tolist()
    data_Low   = df["Low"].tolist()
    data_RSI   = df["RSI"].tolist()

    Entry_Price = df_counter = backtest_pyramiding = unfinished_profit = index_Entry = index_Exit = 0 

    list_NetP      = []
    EntryTimes     = []
    ExitTimes      = []
    list_paperLoss = []

    for index in np.arange(indexLen):
        Close    = data_Close[index]
        Time     = int(data_OpenTime[index])
        RSI      = data_RSI[index]
        LAST_RSI = data_RSI[index-1]

        if side == "L":
            if Rsi_logic.LONG_ENTRY(RSI, LAST_RSI, INPUT_RSI_ENTRY, INPUT_RSI_EXIT, False, backtest_pyramiding):

                index_Entry, Entry_Price, backtest_pyramiding, EntryTimes, Time = \
                BT_module.func_backtest_entry(index, Close, 1, EntryTimes, Time)

            if Rsi_logic.LONG_EXIT(RSI, INPUT_RSI_EXIT, False, backtest_pyramiding):

                index_Exit,Exit_Price,backtest_pyramiding,list_NetP,ExitTimes,list_paperLoss = \
                BT_module.func_backtest_exit(\
                side, index, Close, 0, list_NetP,ExitTimes,list_paperLoss,Time,Entry_Price,index_Entry, index_Exit,data_High,data_Low)

        if side == "S":
            if Rsi_logic.SHORT_ENTRY(RSI, LAST_RSI, INPUT_RSI_ENTRY, INPUT_RSI_EXIT, False, backtest_pyramiding):

                index_Entry, Entry_Price, backtest_pyramiding, EntryTimes, Time = \
                BT_module.func_backtest_entry(index, Close, 1, EntryTimes, Time)

            if Rsi_logic.SHORT_EXIT(RSI, INPUT_RSI_EXIT, False, backtest_pyramiding):

                index_Exit,Exit_Price,backtest_pyramiding,list_NetP,ExitTimes,list_paperLoss = \
                BT_module.func_backtest_exit(\
                side, index, Close, 0,list_NetP,ExitTimes,list_paperLoss,Time,Entry_Price,index_Entry, index_Exit,data_High,data_Low)

        if df_counter == df["Close"].count()-1 and backtest_pyramiding > 0:
            Exit_Price = Close
            backtest_pyramiding = 0
            unfinished_profit = round(((Exit_Price/Entry_Price - 1)*100),2)

        df_counter += 1

    return unfinished_profit, list_NetP, list_paperLoss, EntryTimes, ExitTimes
#____________________________________________________________________________________________________________

def batch(Worker, Strategy, df_kline, TimeFrame, stage):

    def single_backtest(df_kline, TimeFrame, P1, P2, P3):
        
        list_params = [P1, P2, P3]
        unfinished_profit, list_NetP, list_paperLoss, EntryTimes, ExitTimes = \
                run(df_kline.copy(), TimeFrame, Strategy, P1, P2, P3)

        return list_params, unfinished_profit, list_NetP, list_paperLoss, EntryTimes, ExitTimes

    if Strategy == "RsiL":
        P2_min, P2_max, P2_cut = P2_LONG_min, P2_LONG_max, P2_LONG_cut 
    if Strategy == "RsiS":
        P2_min, P2_max, P2_cut = P2_SHORT_min, P2_SHORT_max, P2_SHORT_cut 

    if stage == "DEBUG":
        P1_cut, P2_cut, P3_cut = 6,6,6
    if stage == "TEST":
        P1_cut, P2_cut, P3_cut = 8,8,8

    backtest_result = job.Parallel(n_jobs=Worker, verbose=5)\
                        (job.delayed(single_backtest)\
                        (df_kline, TimeFrame, P1, P2, P3)\
                        for P1 in BT_module.P1_Range(P1_min, P1_max, P1_cut)\
                        for P2 in BT_module.P2_Range(P2_min, P2_max, P2_cut)\
                        for P3 in BT_module.P3_Range(P3_min, P3_max, P3_cut))

    return backtest_result
#____________________________________________________________________________________________________________

if __name__ == "__main__":

    import pandas as pd

    df_kline = pd.read_csv(f"/home/viceversa/Dropbox/bankof3v/static/SAMPLE/kline/kline1m_6h.csv")

    Strategy = "RsiL"
    #Strategy = "RsiS"

    if Strategy == "RsiL":
        INPUT_RSI_ENTRY = 40

    if Strategy == "RsiS":
        INPUT_RSI_ENTRY = 60

    INPUT_RSI_LENGTH = 30
    INPUT_RSI_EXIT = 50

    data = run(df_kline, 5, Strategy, INPUT_RSI_LENGTH, INPUT_RSI_ENTRY, INPUT_RSI_EXIT)

    print(data)

    unfinished_profit = data[0]
    list_NetP = data[1]
    list_paperLoss = data[2]
    EntryTimes = data[3]
    ExitTimes = data[4]

    print(f"EntryTimes {EntryTimes}")
    print(f"ExitTimes {ExitTimes}")
    print(f"list_NetP {list_NetP}")
    print(f"list_paperLoss {list_paperLoss}")
    print(f"unfinished_profit {unfinished_profit}")
    