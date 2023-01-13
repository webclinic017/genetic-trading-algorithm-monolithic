
import sys, pathlib, sqlite3, logging, ast
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/strategy")
import kline
import pandas as pd

import warnings
warnings.simplefilter('ignore', FutureWarning)

#__________________________________________________________________________________


def fetch_params_kline(Session, Symbol, ExchangeID, CandleTimeFrame):

    connection = sqlite3.connect(f"{outside_dir}/bankof3v.db")
    c = connection.cursor()

    c.execute(f"SELECT * FROM {Session} WHERE SYMBOL = '{Symbol}'")
    #_______________________________________________________________
    # PARAMS
    #Get column name.
    column_names = list(map(lambda x: x[0], c.description))
    params_data = c.fetchone()

    df_params = pd.DataFrame([params_data], columns=column_names)

    PARAMS = df_params.loc[0, 'PARAMS']
    PARAMS = ast.literal_eval(PARAMS) # to list from string.

    max_param = max(PARAMS) + 100 # Buffer X bars
    #_______________________________________________________________
    # KLINE
    TableName = kline.tableName(Session, Symbol, ExchangeID, CandleTimeFrame)
    
    c.execute(f"SELECT * FROM {TableName} ORDER BY rowid DESC LIMIT {max_param}")

    kline_column_names = list(map(lambda x: x[0], c.description))

    kline_data = c.fetchall()

    df_kline_from_db = pd.DataFrame(kline_data, columns=kline_column_names)
    
    df_kline_from_db = df_kline_from_db.iloc[::-1]

    return PARAMS, df_kline_from_db

