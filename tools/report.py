import sys, pathlib, time, logging
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/strategy")
sys.path.append(f"{str(working_dir)}/tools")
import vm, discorder

logging.basicConfig(level=logging.INFO,format="%(asctime)s : %(message)s")
#_____________________________________________________________________________________

def error(e, message):

    server = "error"
    embed_title = e

    logging.warning(e)
    try:
        discorder.send(message, embed_title, server = server)
    except Exception as e:
        logging.warning(f"Error. sending Discort ERROR report -> {e}")
#_____________________________________________________________________________________

def backtest(info_type, discord_server, list_Symbol, list_Strategy, timer_symbol, timer_strategy, timer_global,\
                Symbol, Strategy, ActivationTime, symbol_counter, strategy_counter, total_backtest_counter):

    Session = f"{Strategy}{ActivationTime}"

    elapse_symbol = round((time.time() - timer_symbol)/60,1)
    elapse_strategy = round((time.time() - timer_strategy)/60,1)
    elapse_global = round((time.time() - timer_global)/60,1)

    len_list_Strategy = int(len(list_Strategy))
    len_list_Symbol = int(len(list_Symbol))

    total_backtest = len_list_Strategy* len_list_Symbol

    symbols_left = len_list_Symbol - symbol_counter
    average_singele_backtest_time = elapse_strategy/symbol_counter

    estimation_min = float(round(symbols_left * average_singele_backtest_time,1))
    estimation_hour = round(estimation_min/60,1)

    if info_type == "symbol":
        server = discord_server
        title = f"Finished -> {Symbol}/{Strategy}"

        embed_description = f"Progress(Symbol): {symbol_counter}/{len_list_Symbol}\n\
        Progress(Strategy): {strategy_counter}/{len_list_Strategy}\n\
        Progress(Total): {total_backtest_counter}/{total_backtest}\n\
        Elapsed (Symbol), {Symbol}, {elapse_symbol} min.\n\
        Elapsed (Strategy), {Strategy}, {elapse_strategy} min.\n\
        Elapsed (Total), {elapse_global}min.\n\
        Estimation(Strategy), {estimation_min}min ({estimation_hour}/h) to Finish {Strategy}."

    elif info_type == "strategy":
        server = discord_server
        title = f"Finished --->>> {Strategy} <<---"

        embed_description = f"Progress(Strategy): {strategy_counter}/{len_list_Strategy}\n\
        Progress(Total): {total_backtest_counter}/{total_backtest}\n\
        Elapsed (Strategy), {Strategy}, {elapse_strategy} min.\n\
        Elapsed (Total), {elapse_global}min.\n\
        Strategy List ->\n\
        {list_Strategy}\n\
        Symbol List ->\n\
        {list_Symbol}"

    logging.info(embed_description)
    
    try:
        discorder.send(title, Session, embed_description, username = vm.GCP_instance, server = server)
    except Exception as e:
        logging.warning(f"Error. sending backtest report -> {e}")
#_____________________________________________________________________________________

def upload_gcs(exchangeName = "exchangeName Unknown"):

    server = "gcs"
    message = f"Success Upload to GCS -> {exchangeName}"

    logging.info(message)

    try:
        discorder.send(message, server = server)
    except Exception as e:
        logging.warning(f"Error. sending upload_gcs report for {exchangeName} -> {e}")

#_____________________________________________________________________________________

def new_account_data(exchangeName):

    server = "database"
    message = f"Success new position/balance data -> {exchangeName}"
    logging.info(message)
    
    try:
        discorder.send(message, server = server)
    except Exception as e:
        logging.warning(f"Error. sending new_account_data report for {exchangeName} -> {e}")

#_____________________________________________________________________________________

def account(exchangeName, file_path, debug):

    if debug == False:
        
        if exchangeName == "BINANCE":        
            server = "binance_report"

        elif exchangeName == "BINANCETESTNET":
            server = "binancetestnet_report"
    else:
        server = "debug"

    message = f"New report arrived for {exchangeName}!"

    logging.info(f"New report for {exchangeName}")

    try:
        discorder.send(file_path = file_path, server = server)
    except Exception as e:
        logging.warning(f"Error. sending investment report for {exchangeName} -> {e}")
#_____________________________________________________________________________________

def trade_system_log(message, debug = False):

    if debug == False:
        server = "trade_system_log"
    else:
        server = "trade_debug"

    logging.info(message)

    try:
        discorder.send(message, server = server)
    except Exception as e:
        logging.warning(f"Error. sending order report -> {e}")
#_____________________________________________________________________________________


def trade_system_error(message, debug = False):

    if debug == False:
        server = "trade_system_erorr"
    else:
        server = "trade_debug"

    logging.info(message)

    try:
        discorder.send(message, server = server)
    except Exception as e:
        logging.warning(f"Error. sending order report -> {e}")

#_____________________________________________________________________________________

def ORDER(message, embed_title, embed_description, debug = False):

    if debug == False:
        server = "order_message"
    else:
        server = "trade_debug"

    logging.info(message)
    logging.info(embed_title)
    logging.info(embed_description)

    try:

        # if detail == False:
        #     discorder.send(message, server = server)
        # else:
        discorder.send(message, embed_title, embed_description, server = server)

    except Exception as e:
        logging.warning(f"Error. sending order report -> {e}")













if __name__ == "__main__":
    import os

    exchangeName = "BINANCETESTNET"

    LOCAL_path = f"{working_dir}/static/TEMP"

    os.makedirs(LOCAL_path, exist_ok=True)
    file_path = f'{LOCAL_path}/report_{exchangeName}.png'

    account(exchangeName, file_path)