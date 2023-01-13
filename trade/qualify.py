import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
import os, logging, sqlite3
import pandas as pd
from rich.logging import RichHandler
from google.cloud import storage

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")

def run(Strategy, SessionTime, Session, bucket_name, bucket_client, bucket, stage):

    result_columns = {  'PARAMS':[],
                        'UNFINISHED_PROFIT':[],
                        'NET_PROFIT':[],
                        'RESULT_ASSET':[],
                        "PAPER_LOSS":[],
                        'SAMPLE_SIZE':[],
                        'ENTRY_TIMES':[],
                        'EXIT_TIMES':[]}

    df_qualify = pd.DataFrame(columns = result_columns)

    logging.info("Going to qualify. Please wait.")

    for file in bucket_client.list_blobs(bucket_name):

        if ".csv" in file.name and f"{stage}" in file.name and f"{Strategy}" in file.name and f"{SessionTime}" in file.name:
        
            df_result = pd.read_csv(f'gs://{bucket_name}/{file.name}')

            # TODO: Qual Params
            require_trade_freq_days = 3 # once in X days
            MaxAllow_unfinished_profit = -8 # %

            # Setting Require SmapleSize
            backtested_total_days = df_result["DAYS"][0]
            require_SampleSize = int(backtested_total_days/require_trade_freq_days)

            try:
                df_result = df_result.sort_values(by="RESULT_ASSET", ascending=False)
                df_result.drop(df_result.loc[df_result['RESULT_ASSET']<= 100].index, inplace=True)

                #_________________________________________________________________________________________________________
                # FIXME: Disabled for Testing

                df_result.drop(df_result.loc[df_result['UNFINISHED_PROFIT']<= MaxAllow_unfinished_profit].index, inplace=True)
                
                # df_result.drop(df_result.loc[df_result['SAMPLE_SIZE']<=require_SampleSize].index, inplace=True)
                #__________________________________________________________________________________________________________

                df_result.reset_index(drop=True, inplace=True)
                df_s       = df_result.iloc[0]
                df_temp    = pd.DataFrame(df_s).T
                df_qualify = pd.concat([df_qualify, df_temp], axis=0)
                log.info(f"OK. {file.name}")
                
            except Exception as e:
                log.info(f"SKIP. {file.name}. reason -> {e}")
                continue

    # Top 10 Conditions
    df_qualify = df_qualify.sort_values('RESULT_ASSET', ascending = False)
    df_qualify.reset_index(drop = True, inplace = True)

    # YOU MUST WRITE & RE CSV THEN "TO_SQL". Otherwise, Data will be Blob in DB.
    Session = f"{Strategy}_{SessionTime}"

    os.makedirs(f"{working_dir}/static/QUALIFY", exist_ok=True)

    df_qualify.to_csv(f"{working_dir}/static/QUALIFY/{Session}.csv", index=False)

    df_qualify = pd.read_csv(f"{working_dir}/static/QUALIFY/{Session}.csv")
    # _______________________________________________________________________________
    # Insert to bankof3v.db
    
    con = sqlite3.connect(f"{outside_dir}/bankof3v.db")

    df_qualify.to_sql(f'{Session}', con, if_exists='replace', index = False)

    logging.info(f"Database Location @{outside_dir}")

    #---------------------------------------- UPLOAD ----------------------------------------------------------

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"./config/GCP_marketstar.json"
    
    client_storage = storage.Client()
    
    bucket_name = "bankof3v_bucket"
    
    bucket = client_storage.get_bucket(bucket_name)

    GCS_path = f'QUALIFY/{Session}.csv'
    LOCAL_path = f'{working_dir}/static/{GCS_path}'
    
    df_qualify.to_csv(LOCAL_path, index=False)
    
    blob_data = bucket.blob(GCS_path)
    
    blob_data.upload_from_filename(LOCAL_path)
    
    logging.info(f"Successfuly Uploaded QUALIFY Result -> {LOCAL_path}")

    list_symbols = fetch_symbols(Session)

    return list_symbols


#==================================================================
# list_symbols Exracted

def fetch_symbols(Session):

    connection = sqlite3.connect(f"{outside_dir}/bankof3v.db")

    connection.row_factory = lambda cursor, row: row[0]

    c = connection.cursor()

    sql = f"SELECT SYMBOL FROM {Session}"
    c.execute(sql)

    list_symbols = c.fetchall()

    return list_symbols

# TEST #

if __name__ == "__main__": 

    import setup

    SessionInfo = setup.run()

    Session = SessionInfo[2]

    run(SessionInfo[0], SessionInfo[1], Session, SessionInfo[3], SessionInfo[4], SessionInfo[5], SessionInfo[6])

    list_symbols = fetch_symbols(Session)

    print(list_symbols)