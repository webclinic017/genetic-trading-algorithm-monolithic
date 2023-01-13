
import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
import joblib as job
from tqdm import tqdm
from strategy.Devi import Devi_backtest
from strategy.Rsix import Rsi_backtest
import numpy as np
import module
from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

import warnings
warnings.simplefilter('ignore', FutureWarning)
warnings.filterwarnings('ignore')
#______________________________________________________________________________________________________________________________
    

def param2(Worker, Strategy, df_kline, stage):

    def single_backtest(df_kline, P1, P2):
        list_params = [P1, P2]
        EntryTimes, ExitTimes, list_NetP, list_paperLoss, unfinished_profit, sample_size = \
                Rsi_backtest.run(df_kline.copy(), Strategy, P1, P2)
        return list_params, unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes
    
    if Strategy == "RsiL" or Strategy == "RsiS":
        P1_min, P1_max, P1_cut = Rsi_backtest.P1_min, Rsi_backtest.P1_max, Rsi_backtest.P1_cut 
        P2_min, P2_max, P2_cut = Rsi_backtest.P2_SHORT_min, Rsi_backtest.P2_SHORT_max, Rsi_backtest.P2_SHORT_cut 

    if stage == "DEBUG":
        P1_cut, P2_cut = 4,4

    backtest_result = job.Parallel(n_jobs=Worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_kline, P1, P2)\
                        for P1 in tqdm(P1_Range(P1_min, P1_max, P1_cut))\
                        for P2 in P2_Range(P2_min, P2_max, P2_cut))
    return backtest_result

#______________________________________________________________________________________________________________________________


def param3(Worker, Strategy, df_kline, stage):

    def single_backtest(df_kline, P1, P2, P3):
        list_params = [P1, P2, P3]
        unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes = \
                Rsi_backtest.run(df_kline.copy(), Strategy, P1, P2, P3)
        return list_params, unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes

    if Strategy == "RsiL" or Strategy == "RsiS":
        
        P1_min, P1_max, P1_cut = Rsi_backtest.P1_min, Rsi_backtest.P1_max, Rsi_backtest.P1_cut 

        if Strategy == "RsiL":
            P2_min, P2_max, P2_cut = Rsi_backtest.P2_LONG_min, Rsi_backtest.P2_LONG_max, Rsi_backtest.P2_LONG_cut 
        if Strategy == "RsiS":
            P2_min, P2_max, P2_cut = Rsi_backtest.P2_SHORT_min, Rsi_backtest.P2_SHORT_max, Rsi_backtest.P2_SHORT_cut 

        P3_min, P3_max, P3_cut = Rsi_backtest.P3_min , Rsi_backtest.P3_max, Rsi_backtest.P3_cut 

    if stage == "DEBUG":
        P1_cut, P2_cut, P3_cut = 4,4,4
    if stage == "TEST":
        P1_cut, P2_cut, P3_cut = 8,8,8

    backtest_result = job.Parallel(n_jobs=Worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_kline, P1, P2, P3)\
                        for P1 in tqdm(P1_Range(P1_min, P1_max, P1_cut))\
                        for P2 in P2_Range(P2_min, P2_max, P2_cut)\
                        for P3 in P3_Range(P3_min, P3_max, P3_cut))

    return backtest_result

#______________________________________________________________________________________________________________________________


def param4(Worker, Strategy, df_kline, stage):

    def single_backtest(df_kline, P1, P2, P3, P4):
        list_params = [P1, P2, P3, P4]
        unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes = \
            Devi_backtest.run(df_kline.copy(), Strategy, P1, P2, P3, P4)
        return list_params, unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes
    
    if Strategy == "DeviL" or Strategy == "DeviS":
        P1_min, P1_max, P1_cut = Devi_backtest.P1_min,  Devi_backtest.P1_max, Devi_backtest.P1_cut # ATR
        P2_min, P2_max, P2_cut = Devi_backtest.P2_min,  Devi_backtest.P2_max, Devi_backtest.P2_cut # CORE
        P3_min, P3_max, P3_cut = Devi_backtest.P3_min , Devi_backtest.P3_max, Devi_backtest.P3_cut # TR
        P4_min, P4_max, P4_cut = Devi_backtest.P4_min,  Devi_backtest.P4_max, Devi_backtest.P4_cut # TREND
    
    if stage == "DEBUG":
        P1_cut, P2_cut, P3_cut, P4_cut = 4,4,4,4

    backtest_result = job.Parallel(n_jobs=Worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_kline, P1, P2, P3, P4)\
                        for P1 in tqdm(P1_Range(P1_min, P1_max, P1_cut))\
                        for P2 in P2_Range(P2_min, P2_max, P2_cut)\
                        for P3 in P3_Range(P3_min, P3_max, P3_cut)\
                        for P4 in P4_Range(P4_min, P4_max, P4_cut))

    return backtest_result


#__________________________________________________________________

def P1_Range(P1_min, P1_max, P1_cut):
    P1_step  = int((P1_max - P1_min) /P1_cut)
    range_P1 = np.arange(P1_min, P1_max+1, P1_step)
    return range_P1

def P2_Range(P2_min, P2_max, P2_cut):
    P2_step  = int((P2_max - P2_min) /P2_cut)
    range_P2 = np.arange(P2_min, P2_max+1, P2_step)
    return range_P2

def P3_Range(P3_min, P3_max, P3_cut):
    P3_step  = int((P3_max - P3_min) /P3_cut)
    range_P3 = np.arange(P3_min, P3_max+1, P3_step)
    return range_P3

def P4_Range(P4_min, P4_max, P4_cut):
    P4_step = int((P4_max - P4_min) / P4_cut)
    range_P4 = np.arange(P4_min, P4_max+1, P4_step)
    return range_P4