
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
def LONG_ENTRY(Close, Lower, TREND, CloseLast, LowerLast, TrendLast, trading = True, backtest_pyramiding = 0):
    try:
        EntryCondition = Close < Lower and Close > TREND
        LastEntryCondition = CloseLast < LowerLast and CloseLast > TrendLast

        if trading == True:
            if EntryCondition and not LastEntryCondition:
                return True

        # backtest mode
        elif trading == False:
            if EntryCondition and not LastEntryCondition and backtest_pyramiding == 0: 
                return True

    except Exception as e:
        log.warning(f"ERROR in DeviL ENTRY Logic -> {e}")

#___________________________________________________________________________

def LONG_EXIT(Close, CORE, trading = True, backtest_pyramiding = 0):
    try:
        ExitCondition = Close > CORE

        if trading == True:
            if ExitCondition:
                return True

        # backtest mode
        elif trading == False:
            if ExitCondition and backtest_pyramiding != 0:
                return True

    except Exception as e:
        log.warning(f"ERROR in DeviL EXIT Logic -> {e}")

"""
------------------------------- SHORT ---------------------------------
"""

def SHORT_ENTRY(Close, Upper, Trend, CloseLast, UpperLast, TrendLast, trading = True, backtest_pyramiding = 0):
    try:
        EntryCondition = Close > Upper and Close < Trend
        LastEntryCondition = CloseLast > UpperLast and CloseLast < TrendLast

        if trading == True:
            if EntryCondition and not LastEntryCondition:
                return True

        # backtest mode
        elif trading == False:
            if EntryCondition and not LastEntryCondition and backtest_pyramiding == 0: 
                return True

    except Exception as e:
        log.warning(f"ERROR in DeviS ENTRY Logic -> {e}")
#___________________________________________________________________________

def SHORT_EXIT(Close, Core, trading = True, backtest_pyramiding = 0):
    try:
        ExitCondition = Close < Core

        if trading == True:
            if ExitCondition:
                return True

        # backtest mode
        elif trading == False:
            if ExitCondition and backtest_pyramiding != 0:
                return True

    except Exception as e:
        log.warning(f"ERROR in DeviS EXIT Logic -> {e}")