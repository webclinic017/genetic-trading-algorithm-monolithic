import sys, pathlib, os
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/tools")

import time, sys, logging, time, sqlite3, pathlib
from pprint import pprint
from binance import Client
from multiprocessing import Process
import pandas as pd
from config import pw
from tools import gcs, report

from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")
#________________________________________________________
def delete_table(exchangeName):
    con = sqlite3.connect(f"{outside_dir}/bankof3v.db")
    cur = con.cursor()
    cur.execute(f"Drop Table if exists account_{exchangeName}")
    con.close()
    log.info(f"deleted account_{exchangeName}")
#________________________________________________________

def get(exchangeName):
    try:
        if exchangeName == "BINANCETESTNET":
            client = Client(pw.test_binance_api_key, pw.test_binance_api_secret, testnet=True)
        elif exchangeName == "BINANCE":
            client = Client(pw.binance_api_key, pw.binance_api_secret)

        con = sqlite3.connect(f"{outside_dir}/bankof3v.db")
        cur = con.cursor()

        unixtime = int(time.time())

        all_position_data = client.futures_position_information()

        balance_data  = client.futures_account_balance()
        open_position = []

        for i in range(len(all_position_data)):
            positionAmt     = float(all_position_data[i]["positionAmt"])
            if positionAmt != 0:
                open_position.append(all_position_data[i])

        data = [(str(exchangeName), int(unixtime), str(balance_data), str(open_position),),]

        cur.execute(f"CREATE TABLE IF NOT EXISTS account_{exchangeName} (exchangeName, unixtime, balance, position)")

        cur.executemany(f"INSERT INTO account_{exchangeName} VALUES(?,?,?,?)", data)
        con.commit()
        con.close()

        report.new_account_data(exchangeName)

    except Exception as e:

        report.error(e, "Error save_account.py -> Error happend when I'm trying to get new account balance and position data.")
#________________________________________________________

def upload(exchangeName):
    try:
        os.makedirs(f"static/ACCOUNT", exist_ok=True)
        bucket_name  = "bankof3v_bucket"

        con = sqlite3.connect(f"{outside_dir}/bankof3v.db")
        db_df = pd.read_sql_query(f"SELECT * FROM account_{exchangeName}", con)

        GCS_path = f'ACCOUNT/account_{exchangeName}.csv'
        LOCAL_path = f'{working_dir}/static/{GCS_path}'

        db_df.to_csv(LOCAL_path, index=False)

        gcs.upload(bucket_name, LOCAL_path, GCS_path)
        #____________________________________________________

        unixtime = int(time.time())
        GCS_backup_path = f'ACCOUNT/BACKUP/{exchangeName}_{unixtime}.csv'

        gcs.upload(bucket_name, LOCAL_path, GCS_backup_path)

        report.upload_gcs(exchangeName)

    except Exception as e:

        report.error(e, "Error save_account.py -> Error happend when I'm trying to upload account database to GoogleCloudStorage.")


def multi_delete_table():

    p1 = Process(target=delete_table, args=('BINANCE',))
    p2 = Process(target=delete_table, args=('BINANCETESTNET',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
#________________________________________________________

def multi_get():

    p1 = Process(target=get, args=('BINANCE',))
    p2 = Process(target=get, args=('BINANCETESTNET',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
#________________________________________________________

def multi_upload():
    p1 = Process(target=upload, args=('BINANCE',))
    p2 = Process(target=upload, args=('BINANCETESTNET',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

#________________________________________________________

if __name__ == "__main__":
    multi_delete_table()
    multi_get()
    multi_upload()