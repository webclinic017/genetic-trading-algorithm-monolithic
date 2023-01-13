import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))

import Devi_dataframe, Devi_logic
import numpy as np
import joblib as job
from tqdm import tqdm
from benchmark import module as BT_module

from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

import warnings
warnings.simplefilter('ignore', FutureWarning)
#___________________________________________________________________________

paramSize = 4

# ATR
P1_min = 720
P1_max = 720*6
P1_cut = 6

# CORE
P2_min = 360
P2_max = 360*6
P2_cut = 6

# TR
P3_min = 360
P3_max = 360*6
P3_cut = 6

# TREND
P4_min = 1440
P4_max = 14406
P4_cut = 6
"""
-------------------------------  BACKTEST ---------------------------------
"""
def run(df_origin, Strategy, ATR, CORE, TR, TREND):

    df = Devi_dataframe.run(df_origin, ATR, CORE, TR, TREND, False)

    indexLen    = len(df.index)
    data_Time   = df["OpenTime"].tolist()
    data_Close  = df["Close"].tolist()
    data_Low    = df["Low"].tolist()
    data_Upper  = df["Upper"].tolist()
    data_Lower  = df["Lower"].tolist()
    data_Core   = df["CORE"].tolist()
    data_Trend  = df["TREND"].tolist()

    Entry_Price = df_counter = backtest_pyramiding = unfinished_profit = sample_size = index_Entry = index_Exit = 0 

    list_NetP      = []
    EntryTimes     = []
    ExitTimes      = []
    list_paperLoss = []

    for i in np.arange(indexLen):
        Close  = data_Close[i]
        Upper  = data_Upper[i]
        Lower  = data_Lower[i]
        CORE   = data_Core[i]
        TREND  = data_Trend[i]
        Time   = int(data_Time[i])

        CloseLast  = data_Close[i-1]
        UpperLast  = data_Upper[i-1]
        LowerLast  = data_Lower[i-1]
        # CoreLast   = data_Core[i-1]
        TrendLast  = data_Trend[i-1]

        if Strategy == "DeviL":

            # ENTRY, Backtest mode
            if Devi_logic.LONG_ENTRY(Close, Lower, TREND, CloseLast, LowerLast, TrendLast, False, backtest_pyramiding):
                index_Entry = i
                Entry_Price = Close
                backtest_pyramiding = 1
                EntryTimes.append(Time) 

            # EXIT,  Backtest mode
            if Devi_logic.LONG_EXIT(Close, CORE, False, backtest_pyramiding):
                index_Exit = i
                Exit_Price = Close
                backtest_pyramiding = 0

                # https://bobbyhadz.com/blog/python-zerodivisionerror-float-division-by-zero
                temp_NetP_N = Entry_Price and ((Exit_Price/Entry_Price - 1)*100) 

                list_NetP.append(round(temp_NetP_N,2)) 
                ExitTimes.append(Time)

                WorstPrice = Entry_Price
                for x in range(index_Entry, index_Exit):
                    temp_Worst = data_Low[x]
                    if temp_Worst < WorstPrice:
                        WorstPrice = temp_Worst

                paperLoss = (WorstPrice/Entry_Price - 1)*100

                list_paperLoss.append(round(paperLoss,2))

        elif Strategy == "DeviS":

            # ENTRY, Backtest mode
            if Devi_logic.SHORT_ENTRY(Close, Upper, TREND, CloseLast, UpperLast, TrendLast, False, backtest_pyramiding):
                index_Entry = i
                Entry_Price = Close
                backtest_pyramiding = 1
                EntryTimes.append(Time) 

            # EXIT,  Backtest mode
            if Devi_logic.SHORT_EXIT(Close, CORE, False, backtest_pyramiding):
                index_Exit = i
                Exit_Price = Close
                backtest_pyramiding = 0

                # https://bobbyhadz.com/blog/python-zerodivisionerror-float-division-by-zero
                temp_NetP_N = Entry_Price and ((Exit_Price/Entry_Price - 1)*100) 

                list_NetP.append(round(temp_NetP_N,2)) 
                ExitTimes.append(Time)

                WorstPrice = Entry_Price
                for x in range(index_Entry, index_Exit):
                    temp_Worst = data_Low[x]
                    if temp_Worst < WorstPrice:
                        WorstPrice = temp_Worst

                paperLoss = (WorstPrice/Entry_Price - 1)*100

                list_paperLoss.append(round(paperLoss,2))

        # Existing position #
        if df_counter == df["Close"].count()-1 and backtest_pyramiding == 1:
            Exit_Price = Close
            backtest_pyramiding = 0
            unfinished_profit = round(((Exit_Price/Entry_Price - 1)*100),2)

        df_counter += 1

        sample_size = len(ExitTimes)

    return unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes



def batch(Worker, Strategy, df_kline, stage):

    def single_backtest(df_kline, P1, P2, P3, P4):
        list_params = [P1, P2, P3, P4]
        unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes = \
            run(df_kline.copy(), Strategy, P1, P2, P3, P4)
        return list_params, unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes

    if stage == "DEBUG":
        P1_cut, P2_cut, P3_cut, P4_cut = 4,4,4,4

    backtest_result = job.Parallel(n_jobs=Worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_kline, P1, P2, P3, P4)\
                        for P1 in tqdm(BT_module.P1_Range(P1_min, P1_max, P1_cut))\
                        for P2 in BT_module.P2_Range(P2_min, P2_max, P2_cut)\
                        for P3 in BT_module.P3_Range(P3_min, P3_max, P3_cut)\
                        for P4 in BT_module.P4_Range(P4_min, P4_max, P4_cut))

    return backtest_result
