
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
def LONG_ENTRY(RSI, RSI_LAST, RSI_LONG_ENTRY, RSI_EXIT, trading = True, backtest_pyramiding = False):
    #log.warning(f"{RSI},{RSI_LAST},{RSI_LONG_ENTRY}")
    try:
        ENTRY_Cond      = RSI      < RSI_LONG_ENTRY
        LAST_ENTRY_Cond = RSI_LAST < RSI_LONG_ENTRY
        DONT_ENTRY_Cond = RSI_LONG_ENTRY >= RSI_EXIT #if entry is worth than exit. this is exceptional.

        if trading == True:
            if ENTRY_Cond and not LAST_ENTRY_Cond and not DONT_ENTRY_Cond:
                return True

        # backtest mode
        elif trading == False:
            if ENTRY_Cond and not LAST_ENTRY_Cond and not DONT_ENTRY_Cond and backtest_pyramiding == 0: 
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiL ENTRY Logic -> {e}")

#___________________________________________________________________________

def LONG_EXIT(RSI, RSI_EXIT, trading = True, backtest_pyramiding = False):
    try:
        EXIT_Cond = RSI > RSI_EXIT

        if trading == True:
            if EXIT_Cond:
                return True

        # backtest mode
        elif trading == False:
            if EXIT_Cond and backtest_pyramiding != 0:
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiL EXIT Logic -> {e}")

"""
------------------------------- SHORT ---------------------------------
"""

def SHORT_ENTRY(RSI, RSI_LAST, RSI_SHORT_ENTRY, RSI_EXIT, trading = True, backtest_pyramiding = 0):
    try:
        EntryCond      = RSI > RSI_SHORT_ENTRY 
        LastEntryCond  = RSI_LAST > RSI_SHORT_ENTRY 
        DONT_ENTRY_Cond = RSI_SHORT_ENTRY <= RSI_EXIT

        if trading == True:
            if EntryCond and not LastEntryCond and not DONT_ENTRY_Cond:
                return True

        # backtest mode
        elif trading == False:
            if EntryCond and not LastEntryCond  and not DONT_ENTRY_Cond and backtest_pyramiding == 0: 
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiS ENTRY Logic -> {e}")
#___________________________________________________________________________

def SHORT_EXIT(RSI, RSI_EXIT, trading = True, backtest_pyramiding = 0):
    try:
        ExitCond = RSI < RSI_EXIT

        if trading == True:
            if ExitCond:
                return True

        # backtest mode
        elif trading == False:
            if ExitCond and backtest_pyramiding != 0:
                return True

    except Exception as e:
        log.warning(f"ERROR in RsiS EXIT Logic -> {e}")



# ____________________________________________________________________________________________
# ____________________________________________________________________________________________

# test
if __name__ == "__main__":

    RSI         = 30
    RSI_LAST    = 50
    RSI_LONG_ENTRY   = 40
    trading     = False
    backtest_pyramiding = 0

    entry = LONG_ENTRY(RSI, RSI_LAST, RSI_LONG_ENTRY, trading, backtest_pyramiding)

    print(f"entry is ... {entry}")
    #______________________________

    RSI         = 50
    RSI_EXIT    = 40
    backtest_pyramiding = 1

    exit = LONG_EXIT(RSI, RSI_EXIT, trading, backtest_pyramiding)

    print(f"exit is ... {exit}")