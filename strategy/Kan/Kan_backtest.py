import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))
import Kan_dataframe, Kan_logic
from benchmark import module as BT_module
from tqdm import tqdm
import numpy as np
import joblib as job
import warnings
warnings.simplefilter('ignore', FutureWarning)
warnings.filterwarnings('ignore')

# P1 VWMA_LENGTH 
# P2 DEVI_ENTRY
# P3 TAKE_PROFIT_RATIO
# P4 STOP_LOSS_RATIO

P1_LONG_min, P1_LONG_max, P1_LONG_cut = 360, 1440, 8
P2_LONG_min, P2_LONG_max, P2_LONG_cut = -4, -1,   8
P3_LONG_min, P3_LONG_max, P3_LONG_cut =  1,  4,   8
P4_LONG_min, P4_LONG_max, P4_LONG_cut = -4, -1,   8

# P1_SHORT_min, P1_SHORT_max, P1_SHORT_cut 
# P2_SHORT_min, P2_SHORT_max, P2_SHORT_cut 
# P3_SHORT_min, P3_SHORT_max, P3_SHORT_cut 
# P4_SHORT_min, P4_SHORT_max, P4_SHORT_cut 
#____________________________________________________________________________________________________________

def run(df_kline, tf, side, VWMA_LENGTH, DEVI_ENTRY, TAKE_PROFIT_RATIO, STOP_LOSS_RATIO):

    df = Kan_dataframe.run(df_kline, tf, VWMA_LENGTH, DEVI_ENTRY,  False)

    indexLen        = len(df)
    data_OpenTime   = df["OpenTime"].tolist()
    data_Close      = df["Close"].tolist()
    data_High       = df["High"].tolist()
    data_Low        = df["Low"].tolist()
    data_VWMA_DEVI  = df["VWMA_DEVI"].tolist()

    Entry_Price = df_counter = backtest_pyramiding = unfinished_profit = index_Entry = index_Exit = 0 

    list_Profit    = []
    EntryTimes     = []
    ExitTimes      = []
    list_paperLossMAX = []
    list_paperProfitMAX = []

    for index in np.arange(indexLen):
        TIME            = int(data_OpenTime[index])
        CLOSE           = data_Close[index]
        LAST_CLOSE      = data_Close[index-1]
        VWMA_DEVI       = data_VWMA_DEVI[index]
        LAST_VWMA_DEVI  = data_VWMA_DEVI[index-1]

        if side == True:
            if Kan_logic.LONG_ENTRY(CLOSE, VWMA_DEVI, LAST_CLOSE, LAST_VWMA_DEVI, False, backtest_pyramiding):
                index_Entry = index
                Entry_Price = CLOSE
                backtest_pyramiding = 1
                EntryTimes.append(TIME) 

            NET_PROFIT_RATIO = 0

            if backtest_pyramiding != 0:
                NET_PROFIT_RATIO = (1-(Entry_Price/CLOSE))*100 # for LONG

            if Kan_logic.LONG_EXIT(TAKE_PROFIT_RATIO, STOP_LOSS_RATIO, NET_PROFIT_RATIO, False, backtest_pyramiding):

                if NET_PROFIT_RATIO != 0:
                    index_Exit = index
                    Exit_Price = CLOSE
                    backtest_pyramiding = 0

                    ExitTimes.append(TIME)

                    WorstPrice = Entry_Price
                    BestPrice = Entry_Price

                    for x in range(index_Entry, index_Exit):

                        # temp_Best = data_High[x] if side == "L" else data_Low[x]
                        if side == True:
                            temp_Best = data_High[x]
                            temp_Worst = data_Low[x]  
                            if temp_Worst < WorstPrice:
                                WorstPrice = temp_Worst 
                            if temp_Best > BestPrice:
                                BestPrice = temp_Best
                        else:
                            temp_Best = data_Low[x] 
                            temp_Worst = data_High[x]
                            if temp_Worst > WorstPrice:
                                WorstPrice = temp_Worst 
                            if temp_Best < BestPrice:
                                BestPrice = temp_Best

                    if side == True:
                        Profit = (1-(Entry_Price/Exit_Price))*100 
                        paperProfitMAX = (1-(Entry_Price/BestPrice))*100
                        paperLossMAX = (1-(Entry_Price/WorstPrice))*100
                    else:
                        Profit = ((Entry_Price/Exit_Price)-1)*100 
                        paperProfitMAX = ((Entry_Price/BestPrice)-1)*100
                        paperLossMAX = ((Entry_Price/WorstPrice)-1)*100     

                    list_Profit.append(round(Profit,2))
                    list_paperProfitMAX.append(round(paperProfitMAX,2))
                    list_paperLossMAX.append(round(paperLossMAX,2))

        if df_counter == df["Close"].count()-1 and backtest_pyramiding > 0:
            Exit_Price = CLOSE
            backtest_pyramiding = 0
            unfinished_profit = round(((Exit_Price/Entry_Price - 1)*100),2)

        df_counter += 1

    return unfinished_profit, list_Profit, list_paperProfitMAX, list_paperLossMAX, EntryTimes, ExitTimes


def batch(core, side, df_kline, tf, debug):

    def single_backtest(df_kline, tf, P1, P2, P3, P4):
        
        list_params = [P1, P2, P3, P4]

        unfinished_profit, list_Profit, list_paperProfitMAX, list_paperLossMAX, EntryTimes, ExitTimes = \
                run(df_kline.copy(), tf, side, P1, P2, P3, P4)

        return list_params, unfinished_profit, list_Profit, list_paperProfitMAX, list_paperLossMAX, EntryTimes, ExitTimes

    if side == True:
        P1_min, P1_max, P1_cut = P1_LONG_min, P1_LONG_max, P1_LONG_cut 
        P2_min, P2_max, P2_cut = P2_LONG_min, P2_LONG_max, P2_LONG_cut 
        P3_min, P3_max, P3_cut = P3_LONG_min, P3_LONG_max, P3_LONG_cut 
        P4_min, P4_max, P4_cut = P4_LONG_min, P4_LONG_max, P4_LONG_cut 
    # else:
    #     P1_min, P1_max, P1_cut = P1_SHORT_min, P1_SHORT_max, P1_SHORT_cut 
    #     P2_min, P2_max, P2_cut = P2_SHORT_min, P2_SHORT_max, P2_SHORT_cut 
    #     P3_min, P3_max, P3_cut = P3_SHORT_min, P3_SHORT_max, P3_SHORT_cut 
    #     P4_min, P4_max, P4_cut = P4_SHORT_min, P4_SHORT_max, P4_SHORT_cut 

    if debug == True:
        P1_cut, P2_cut, P3_cut, P4_cut = 3,3,3,3

    backtest_result = job.Parallel(n_jobs=core, verbose=5)\
                        (job.delayed(single_backtest)\
                        (df_kline, tf, P1, P2, P3, P4)\
                        for P1 in BT_module.P1_Range(P1_min, P1_max, P1_cut)\
                        for P2 in BT_module.P2_Range(P2_min, P2_max, P2_cut)\
                        for P3 in BT_module.P3_Range(P3_min, P3_max, P3_cut)\
                        for P4 in BT_module.P4_Range(P4_min, P4_max, P4_cut))

    return backtest_result

if __name__ == "__main__":

    import pandas as pd

    try:
        df_kline = pd.read_csv(f"/home/daiki/Dropbox/bankof3v/static/SAMPLE/kline/kline1m_5days.csv")
    except:
        df_kline = pd.read_csv(f"/home/viceversa/Dropbox/bankof3v/static/SAMPLE/kline/kline1m_5days.csv")

    Strategy = "KanL"

    # VWMA_LENGTH         = 720
    # DEVI_ENTRY          = -1.5
    # TAKE_PROFIT_RATIO   = 1.5
    # STOP_LOSS_RATIO     = -1.5

    VWMA_LENGTH         = 0
    DEVI_ENTRY          = 0
    TAKE_PROFIT_RATIO   = 0
    STOP_LOSS_RATIO     = 0

    unfinished_profit, list_Profit, list_paperProfitMAX, list_paperLossMAX, EntryTimes, ExitTimes\
    = run(df_kline, 1, Strategy, VWMA_LENGTH, DEVI_ENTRY, TAKE_PROFIT_RATIO, STOP_LOSS_RATIO)

    # list_params = data[0]
    # unfinished_profit = data[1]
    # list_Profit = data[2]
    # list_paperProfitMAX = data[3]
    # list_paperLossMAX = data[4]
    # EntryTimes = data[5]
    # ExitTimes = data[6]

    print(f"EntryTimes {EntryTimes}")
    print(f"ExitTimes {ExitTimes}")
    print(f"list_Profit {list_Profit}")
    print(f"list_paperProfitMAX {list_paperProfitMAX}")
    print(f"list_paperLossMAX {list_paperLossMAX}")
    print(f"unfinished_profit {unfinished_profit}")
    
    # -------------------------------------------------------------------

    # import matplotlib.pyplot as plt

    # df = pd.DataFrame()
    # df['OpenTime'] = ExitTimes
    # df['OpenTime'] = pd.to_datetime((df['OpenTime']/1000).astype(int), unit='s')
    # xaxis_dt = df['OpenTime'].to_list()

    # xaxis = list(range(1,len(ExitTimes)+1))

    # plt.bar(xaxis, list_paperLossMAX,   width=0.7, edgecolor='k', tick_label=xaxis_dt, label='paperLossMAX')
    # plt.bar(xaxis, list_paperProfitMAX, width=0.7, edgecolor='k', tick_label=xaxis_dt, label='paperProfitMAX')
    # plt.bar(xaxis, list_Profit,         width=0.3, edgecolor='k', tick_label=xaxis_dt, label='Profit')

    # plt.legend()

    # plt.gcf().autofmt_xdate()
    # plt.show()

    # -------------------------------------------------------------------

    # core    = 4
    # side    = True
    # tf      = 1
    # debug   = True

    # backtest_result = batch(core, side, df_kline, tf, debug)

    # df_backtest_result = BT_module.create_df_backtest(backtest_result)

    # df_backtest_result.to_csv("test.csv")


