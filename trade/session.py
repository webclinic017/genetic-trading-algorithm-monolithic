import time, sys, logging, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/strategy")
import module, order
from timeout_decorator import timeout, TimeoutError
import schedule

from strategy.Devi import Devi_trading
from strategy.Rsix import Rsi_trading

from datetime import datetime, timedelta, time
import time
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

################################################################################
# LOGIC

def session_logic(ExchangeClient, Session, SessionPhase, ExchangeID, CandleTimeFrame, list_symbols):
    try:
        session_dead_list = []
        for Symbol in list_symbols:
            try:
                PARAMS, df_kline_from_db = module.fetch_params_kline(Session, Symbol, ExchangeID, CandleTimeFrame)
                #______________________________________________________________________________________________
                # TODO: Devi / Rsi / ... add.
                if "DeviL_" in Session or "DeviS_" in Session:
                    ENTRY_logic, EXIT_logic = Devi_trading.run(PARAMS, df_kline_from_db, Session)
                    
                if "RsiL_" in Session or "RsiS_" in Session:
                    ENTRY_logic, EXIT_logic = Rsi_trading.run(PARAMS, df_kline_from_db, Session)
                #______________________________________________________________________________________________

                dead_or_alive = order.run(ExchangeClient, Symbol, Session, SessionPhase, ENTRY_logic, EXIT_logic)

                session_dead_list.append(dead_or_alive)            

                if all(session_dead_list) == True and len(session_dead_list) == len(list_symbols):
                    print(f"All Symbols are Dead. Thus, This Session {Session} is going to die. good bye.")
                    quit()
                
            except Exception as e:
                log.warning(f"ERROR in Strategy... {Session} {Symbol}... {e}")
                continue

        print(f"Session Dead Count -> {session_dead_list.count(True)}/{len(list_symbols)}")

    except Exception as e:
        log.info(f"ERROR -> {e}")


################################################################################
# Alive & Dying session

SessionDays = 5
SessionInterval = 30

@timeout(SessionDays * 86400)
def alive_phase(ExchangeClient, Session, SessionPhase, ExchangeID, CandleTimeFrame, list_symbols):

    log.info(f"Session starting @{Session}")

    # Maybe, I dont want to trade every 10s. But It's fine. because, if contracts != 0, no entry anyway.
    schedule.every(SessionInterval).seconds.\
        do(session_logic, ExchangeClient, Session, SessionPhase, ExchangeID, CandleTimeFrame, list_symbols).\
        tag('scheduleTag_ALIVE')

    while True:
        schedule.run_pending()
        time.sleep(1)

def dying_phase(ExchangeClient, Session, SessionPhase, ExchangeID, CandleTimeFrame, list_symbols):

    log.info(f"Dying session starting @{Session}")

    schedule.every(SessionInterval).seconds.\
        do(session_logic, ExchangeClient, Session, SessionPhase, ExchangeID, CandleTimeFrame, list_symbols).\
        tag('scheduleTag_DYING')
    
    while True:
        schedule.run_pending()
        time.sleep(1)

################################################################################
# Combine and make it work! 

def run(ExchangeClient, Session, ExchangeID, CandleTimeFrame, list_symbols):

    alive = True

    try:
        alive_phase(ExchangeClient, Session, alive, ExchangeID, CandleTimeFrame, list_symbols)
    # Need timeout exception to timeout Alive-phase properly.
    except TimeoutError:
        log.info("Alive Phase is Timeout")

    # Quit Alive schedule. Without this code, alive-phase remains on dying phase.
    schedule.clear('scheduleTag_ALIVE')

    alive = False
    
    dying_phase(ExchangeClient, Session, alive, ExchangeID, CandleTimeFrame, list_symbols)

#_______________________________________________________________________________________________________

# TEST RUN #
if __name__ == "__main__":

    import setup

    SessionInfo = setup.run()

    print(SessionInfo)

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

    list_symbols = ["BTCUSDT", "ETHUSDT"]

    run(ExchangeClient, Session, ExchangeID, CandleTimeFrame, list_symbols)









