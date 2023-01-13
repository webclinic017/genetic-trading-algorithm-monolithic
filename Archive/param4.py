
import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
import joblib as job
from tqdm import tqdm
import param_range
from strategy.Devi import Devi_backtest
import module
from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")
import warnings
warnings.simplefilter('ignore', FutureWarning)


def run(Worker, Symbol, Strategy, df_origin, days, start, end, stage):

    def single_backtest(df_origin, P1, P2=False, P3=False, P4=False):

        list_params = [P1, P2, P3, P4]

        EntryTimes, ExitTimes, list_NetP, list_paperLoss, unfinished_profit, sample_size = \
            Devi_backtest.run(df_origin.copy(), Strategy, P1, P2, P3, P4)


        return list_params, unfinished_profit, list_NetP, list_paperLoss, sample_size, EntryTimes, ExitTimes
    #______________________________________________________________________________________________________________________________
    
    # preset params
    if Strategy == "DeviL" or Strategy == "DeviS":
        P1_min, P1_max, P1_cut = Devi_backtest.P1_min,  Devi_backtest.P1_max, Devi_backtest.P1_cut # ATR
        P2_min, P2_max, P2_cut = Devi_backtest.P2_min,  Devi_backtest.P2_max, Devi_backtest.P2_cut # CORE
        P3_min, P3_max, P3_cut = Devi_backtest.P3_min , Devi_backtest.P3_max, Devi_backtest.P3_cut # TR
        P4_min, P4_max, P4_cut = Devi_backtest.P4_min,  Devi_backtest.P4_max, Devi_backtest.P4_cut # TREND
    
        if stage == "DEBUG":
            P1_cut, P2_cut, P3_cut, P4_cut = 4,4,4,4

    list_range_1st, list_step   = create_range_1st( P1_min, P1_max, P1_cut,\
                                                    P2_min, P2_max, P2_cut,\
                                                    P3_min, P3_max, P3_cut,\
                                                    P4_min, P4_max, P4_cut)
    
    backtestResultData_1st      = param_job(Worker, single_backtest, df_origin, list_range_1st)

    df_backtestResult_1st       = module.create_backtest_result_df(backtestResultData_1st)

    # 2nd stage
    # list_range_2nd              = create_range_2nd(df_backtestResult_1st,   list_step[0], int(P1_cut/2),\
    #                                                                         list_step[1], int(P2_cut/2),\
    #                                                                         list_step[2], int(P3_cut/2),\
    #                                                                         list_step[3], int(P4_cut/2))

    # backtestResultData_2nd      = param_job(Worker, single_backtest, df_origin, list_range_2nd)

    # df_backtestResult_2nd       = module.create_backtest_result_df(backtestResultData_2nd)

    df_backtestResult           = module.create_df_backtest(Symbol, Strategy, days, start, end, df_backtestResult_1st)

    return df_backtestResult
#________________________________________________________________________________________________________________________________________________

def param_job(Worker, single_backtest, df_origin, list_range):

    range_P1 = list_range[0]
    range_P2 = list_range[1]
    range_P3 = list_range[2]
    range_P4 = list_range[3]

    result = job.Parallel(n_jobs=Worker, verbose=7)\
                        (job.delayed(single_backtest)\
                        (df_origin, P1, P2, P3, P4)\
                        for P1 in tqdm(range_P1)\
                        for P2 in range_P2\
                        for P3 in range_P3\
                        for P4 in range_P4)
    return result

#_______________________________________________________________________________________________________________________________________________

def create_range_1st(   P1_min, P1_max, P1_cut,\
                        P2_min, P2_max, P2_cut,\
                        P3_min, P3_max, P3_cut,\
                        P4_min, P4_max, P4_cut):

    P1_range, P1_step = param_range.P1_Range(P1_min, P1_max, P1_cut)
    P2_range, P2_step = param_range.P2_Range(P2_min, P2_max, P2_cut)
    P3_range, P3_step = param_range.P3_Range(P3_min, P3_max, P3_cut)
    P4_range, P4_step = param_range.P4_Range(P4_min, P4_max, P4_cut)

    list_range = [P1_range, P2_range, P3_range, P4_range]
    list_step  = [P1_step, P2_step, P3_step, P4_step]

    return list_range, list_step

#___________________________________________________________________________

def create_range_2nd(df_result,\
                    P1_step_1st, P1_cut_2nd,\
                    P2_step_1st, P2_cut_2nd,\
                    P3_step_1st, P3_cut_2nd,\
                    P4_step_1st, P4_cut_2nd):

    list_BEST_Params_1st = param_range.create_BEST_params_list(df_result)

    P1_range_2nd = param_range.best_P1_Range(P1_step_1st, list_BEST_Params_1st[0], P1_cut_2nd)
    P2_range_2nd = param_range.best_P2_Range(P2_step_1st, list_BEST_Params_1st[1], P2_cut_2nd)
    P3_range_2nd = param_range.best_P3_Range(P3_step_1st, list_BEST_Params_1st[2], P3_cut_2nd)
    P4_range_2nd = param_range.best_P4_Range(P4_step_1st, list_BEST_Params_1st[3], P4_cut_2nd)

    list_range_2nd = [P1_range_2nd, P2_range_2nd, P3_range_2nd, P4_range_2nd]
    
    return list_range_2nd

