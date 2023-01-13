
import sys, pathlib, logging, warnings
warnings.simplefilter('ignore', FutureWarning)

outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(str(project_dir))
sys.path.append(str(current_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/trade")

import Devi_dataframe, Devi_logic


def run(PARAMS, df_kline_from_db, Session, testmode = False):

    P1_ATR     = PARAMS[0]
    P2_CORE    = PARAMS[1]
    P3_TR      = PARAMS[2]
    P4_TREND   = PARAMS[3]
    
    df = Devi_dataframe.run(df_kline_from_db, P1_ATR, P2_CORE, P3_TR, P4_TREND)

    Upper = df['Upper'].iloc[-1]
    Lower = df['Lower'].iloc[-1]
    CORE  = df['CORE'].iloc[-1]
    TREND = df['TREND'].iloc[-1]
    Close = df['Close'].iloc[-1]

    UpperLast = df['Upper'].iloc[-2]
    LowerLast = df['Lower'].iloc[-2]
    # CoreLast = df['CORE'].iloc[-2]
    TrendLast = df['TREND'].iloc[-2]
    CloseLast = df['Close'].iloc[-2]

    if "DeviL" in Session:
        if Devi_logic.LONG_ENTRY(Close, Lower, TREND, CloseLast, LowerLast, TrendLast):
            ENTRY_logic = True
        else:
            ENTRY_logic = False

        if Devi_logic.LONG_EXIT(Close, CORE):
            EXIT_logic = True
        else:
            EXIT_logic = False

    if "DeviS" in Session:
        if Devi_logic.SHORT_ENTRY(Close, Upper, TREND, CloseLast, UpperLast, TrendLast):
            ENTRY_logic = True
        else:
            ENTRY_logic = False

        if Devi_logic.SHORT_EXIT(Close, CORE):
            EXIT_logic = True
        else:
            EXIT_logic = False
    
    if testmode == True:
        # FIXME: TEST ENTRY
        ENTRY_logic = True
        EXIT_logic = False  

    return ENTRY_logic, EXIT_logic