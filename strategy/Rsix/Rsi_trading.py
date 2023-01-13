
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
import Rsi_dataframe, Rsi_logic

#__________________________________________________________________________

def run(PARAMS, df_kline_from_db, Session, testmode = False):

    RSI_LENGTH = PARAMS[0]
    RSI_ENTRY  = PARAMS[1]
    RSI_EXIT   = PARAMS[2]

    df_Rsi = Rsi_dataframe.run(df_kline_from_db, RSI_LENGTH)

    RSI      = df_Rsi['RSI'].iloc[-1]
    LAST_RSI = df_Rsi['RSI'].iloc[-2]

    if "RsiL" in Session:
        if Rsi_logic.LONG_ENTRY(RSI, LAST_RSI, RSI_ENTRY):
            ENTRY_logic = True
        else:
            ENTRY_logic = False

        if Rsi_logic.LONG_EXIT(RSI, RSI_EXIT):
            EXIT_logic = True
        else:
            EXIT_logic = False

    if "RsiS" in Session:
        if Rsi_logic.SHORT_ENTRY(RSI, LAST_RSI, RSI_ENTRY):
            ENTRY_logic = True
        else:
            ENTRY_logic = False

        if Rsi_logic.SHORT_EXIT(RSI, RSI_EXIT):
            EXIT_logic = True
        else:
            EXIT_logic = False
    
    if testmode == True:
        # FIXME: TEST ENTRY
        ENTRY_logic = True
        EXIT_logic = False  

    return ENTRY_logic, EXIT_logic

#_________________________________________

if __name__ == "__main__":

    from trade import setup

    SessionInfo = setup.run()

    Strategy        = SessionInfo[0]
    SessionTime     = SessionInfo[1]
    Session         = SessionInfo[2]
    bucket_name     = SessionInfo[3]
    bucket_client   = SessionInfo[4]
    bucket          = SessionInfo[5]
    stage           = SessionInfo[6]
    ExchangeID      = SessionInfo[7]
    CandleTimeFrame = SessionInfo[8]
    ExchangeClient  = SessionInfo[9]

    # run(PARAMS, df_kline_from_db, Session, testmode = False)