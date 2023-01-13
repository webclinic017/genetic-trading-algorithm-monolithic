
import sys, pathlib, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))

from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

import warnings
warnings.simplefilter('ignore', FutureWarning)
"""
------------------------------- LONG ---------------------------------
"""
def LONG_ENTRY(CLOSE, ENTRY_PRICE, LAST_CLOSE, LAST_ENTRY_PRICE, trading = True, backtest_pyramiding = False):
    #log.warning(f"{RSI},{RSI_LAST},{RSI_LONG_ENTRY}")
    try:
        ENTRY_Cond      = CLOSE      < ENTRY_PRICE
        LAST_ENTRY_Cond = LAST_CLOSE < LAST_ENTRY_PRICE #FIXME: is this ok? what if there is no last price... such as the first row.

        if trading == True:
            if ENTRY_Cond and not LAST_ENTRY_Cond:
                return True

        # backtest mode
        elif trading == False:
            if ENTRY_Cond and not LAST_ENTRY_Cond and backtest_pyramiding == 0: 
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiL ENTRY Logic -> {e}")

#___________________________________________________________________________

def LONG_EXIT(TAKE_PROFIT_RATIO, STOP_LOSS_RATIO, NET_PROFIT_RATIO, trading = True, backtest_pyramiding = False):
    try:
        TP = NET_PROFIT_RATIO > TAKE_PROFIT_RATIO
        SL = NET_PROFIT_RATIO < STOP_LOSS_RATIO

        if trading == True:
            if TP or SL:
                return True

        # backtest mode
        elif trading == False:
            if TP or SL and backtest_pyramiding != 0:
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiL EXIT Logic -> {e}")

"""
------------------------------- SHORT ---------------------------------
"""

def SHORT_ENTRY(CLOSE, ENTRY_PRICE, LAST_CLOSE, LAST_ENTRY_PRICE, trading = True, backtest_pyramiding = False):
    #log.warning(f"{RSI},{RSI_LAST},{RSI_LONG_ENTRY}")
    try:
        ENTRY_Cond      = CLOSE      > ENTRY_PRICE
        LAST_ENTRY_Cond = LAST_CLOSE > LAST_ENTRY_PRICE

        if trading == True:
            if ENTRY_Cond and not LAST_ENTRY_Cond:
                return True

        # backtest mode
        elif trading == False:
            if ENTRY_Cond and not LAST_ENTRY_Cond and backtest_pyramiding == 0: 
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiL ENTRY Logic -> {e}")

#___________________________________________________________________________

def SHORT_EXIT(TAKE_PROFIT_RATIO, STOP_LOSS_RATIO, NET_PROFIT_RATIO, trading = True, backtest_pyramiding = False):
    try:
        TP = NET_PROFIT_RATIO < TAKE_PROFIT_RATIO
        SL = NET_PROFIT_RATIO > STOP_LOSS_RATIO

        if trading == True:
            if TP or SL:
                return True

        # backtest mode
        elif trading == False:
            if TP or SL and backtest_pyramiding != 0:
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiL EXIT Logic -> {e}")


# ____________________________________________________________________________________________
# ____________________________________________________________________________________________

# test
if __name__ == "__main__":
    trading = False

    backtest_pyramiding = 0

    CLOSE            = 150
    ENTRY_PRICE      = 151 #xu entry line -> short entry
    LAST_CLOSE       = None#150
    LAST_ENTRY_PRICE = None#149

    entry = LONG_ENTRY(CLOSE, ENTRY_PRICE, LAST_CLOSE, LAST_ENTRY_PRICE, trading = True, backtest_pyramiding = False)
    print(f"long entry is ... {entry}")

    CLOSE            = 150
    ENTRY_PRICE      = 149 # xo entry line -> short entry
    LAST_CLOSE       = 150
    LAST_ENTRY_PRICE = 151

    entry = SHORT_ENTRY(CLOSE, ENTRY_PRICE, LAST_CLOSE, LAST_ENTRY_PRICE, trading = True, backtest_pyramiding = False)
    print(f"short entry is ... {entry}")

    #______________________________

    backtest_pyramiding = 1

    TAKE_PROFIT_RATIO = 2
    STOP_LOSS_RATIO   = -2
    NET_PROFIT_RATIO  = 3

    exit = LONG_EXIT(TAKE_PROFIT_RATIO, STOP_LOSS_RATIO, NET_PROFIT_RATIO, trading = True, backtest_pyramiding = False)
    print(f"long exit is ... {exit}")

    TAKE_PROFIT_RATIO = 2
    STOP_LOSS_RATIO   = -2
    NET_PROFIT_RATIO  = -4

    exit = SHORT_EXIT(TAKE_PROFIT_RATIO, STOP_LOSS_RATIO, NET_PROFIT_RATIO, trading = True, backtest_pyramiding = False)
    print(f"short exit is ... {exit}")
