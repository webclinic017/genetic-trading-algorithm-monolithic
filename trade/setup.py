import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
from config import pw
import inquirer, os
from google.api_core import page_iterator
from google.cloud import storage 
from binance.client import Client

#____________________________________________________________________________________________________ 

def _item_to_value(iterator, item):
    return item

def backtest_sessions(bucket_name, prefix):
    if prefix and not prefix.endswith('/'):
        prefix += '/'

    extra_params = {
        "projection": "noAcl",
        "prefix": prefix,
        "delimiter": '/'}

    gcs = storage.Client()

    path = "/b/" + bucket_name + "/o"

    iterator = page_iterator.HTTPIterator(
        client=gcs,
        api_request=gcs._connection.api_request,
        path=path,
        items_key='prefixes',
        item_to_value=_item_to_value,
        extra_params=extra_params,)

    dir_list_tmp = []

    for dir in iterator:
        dir = dir.replace(prefix,"").replace("/","")
        dir_list_tmp.append(dir)

    dir_list= []

    for dir in reversed(dir_list_tmp):
        dir_list.append(dir)

    return dir_list

#____________________________________________________________________________________________________ 

def run():
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{working_dir}/config/GCP_marketstar.json"

    project_id  = "MarketStar"
    bucket_name = "bankof3v_bucket"
    bucket_client = storage.Client(project_id)
    bucket      = bucket_client.get_bucket(bucket_name)

    stage_questions  = [inquirer.List('stage', message="Which Stage?", choices=["DEBUG", "TEST",'PRODUCTION'],),]
    stage_answers    = inquirer.prompt(stage_questions)
    stage            = stage_answers["stage"]

    # TODO:
    list_Strategy = ["DeviL", "DeviS", "RsiL", "RsiS"]

    Strategy_questions = [inquirer.List('Strategy', message="Which Strategy?", choices=list_Strategy,),]
    Strategy_answers   = inquirer.prompt(Strategy_questions)
    Strategy           = Strategy_answers["Strategy"]

    # Fetch Backtest Sessions from GCS bucket #
    prefix = f'{stage}/{Strategy}'

    session_list = backtest_sessions(bucket_name, prefix)

    Session_questions = [inquirer.List('Session', message="Which Session?", choices=session_list,),]
    Session_answers   = inquirer.prompt(Session_questions)
    SessionTime       = Session_answers["Session"]

    ExchangeID_questions = [inquirer.List('ExchangeID', message="Which Exchange?", choices=["BINANCETESTNET", "BINANCE"],),]
    ExchangeID_answers   = inquirer.prompt(ExchangeID_questions)
    ExchangeID           = ExchangeID_answers["ExchangeID"]

    CandleTimeFrame_questions = [inquirer.List('CandleTimeFrame', message="Which CandleTimeFrame?", choices=["1m", "5m", "15m"],),]
    CandleTimeFrame_answers   = inquirer.prompt(CandleTimeFrame_questions)
    CandleTimeFrame           = CandleTimeFrame_answers["CandleTimeFrame"]

    Session = f"{Strategy}_{SessionTime}"

    if ExchangeID == "BINANCE":
        ExchangeClient = Client(pw.binance_api_key, pw.binance_api_secret)

    elif ExchangeID == "BINANCETESTNET":
        ExchangeClient = Client(pw.test_binance_api_key, pw.test_binance_api_secret, {"timeout": 10}, testnet = True)

    #_____________________________________________
    return Strategy, SessionTime, Session, bucket_name, bucket_client, bucket, stage, ExchangeID, CandleTimeFrame, ExchangeClient

#____________________________________________________________________________________________________ 

if __name__ == "__main__": 

    SessionInfo = run()

    print(SessionInfo)

    Strategy    = SessionInfo[0]
    SessionTime = SessionInfo[1]
    Session     = SessionInfo[2]
    bucket_name =  SessionInfo[3]
    bucket_client = SessionInfo[4]
    bucket      = SessionInfo[5]
    stage       = SessionInfo[6]
    ExchangeID  =  SessionInfo[7]
    CandleTimeFrame =  SessionInfo[8]
    ExchangeClient  = SessionInfo[9]

    print(f"{SessionInfo[6]}, {SessionInfo[2]}")