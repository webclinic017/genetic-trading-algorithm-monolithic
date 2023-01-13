import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent  
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
import os
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Timestamp # Don't remove
import numpy as np
import datetime, logging
from strategy import DeviL

logging.basicConfig(level=logging.INFO,format="%(asctime)s : %(message)s")

# TODO: This system going to be ploted by Chart.js (bankof3v.com)

def plot_indicator(Strategy):

    os.makedirs(f"{working_dir}/static/indicator/", exist_ok=True)

    try:
        df_useme = pd.read_csv(f"{working_dir}/static/indicator/latest.csv")

        row_count, col_count = df_useme.shape    

        ncol = 1
        nrow = int(np.ceil(row_count/ncol))

        print(f"ncol = {ncol}, nrow = {nrow}")
        plt.figure(figsize=(30,180))

        for i, (row) in enumerate(df_useme.iterrows()):

            print(f"{i} / {row_count}")
            print("into the loop")

            symbol  = df_useme["Ticker"][i] 
            atr     = df_useme["ATR"][i] 
            tr      = df_useme["TR"][i] 
            core    = df_useme["Core"][i] 
            trend   = df_useme["Trend"][i] 

            print(f"target -> {symbol}")

            df = pd.read_csv(f"remorder/stream_db/{symbol}.csv")

            df = DeviL.create_df(df, tr, atr, trend, core)
            
            show_range = int(1440*3)

            df['OpenTime'] = df['OpenTime']/1000
            df['OpenTime'] = pd.to_datetime(df['OpenTime'].astype(int), unit='s')

            x_opentime = df['OpenTime'].tail(show_range)
            y_close = df['Close'].tail(show_range)
            y_trend = df['Trend'].tail(show_range)
            y_upper = df['Upper'].tail(show_range)
            y_lower = df['Lower'].tail(show_range)
            y_core  = df['Core'].tail(show_range)

            plt.plot(x_opentime,y_close)
            plt.plot(x_opentime,y_trend)
            plt.plot(x_opentime,y_upper)
            plt.plot(x_opentime,y_lower)
            plt.plot(x_opentime,y_core)

            #plt.legend(loc = 'lower right') 

            plt.title(symbol)

            plt.gcf().autofmt_xdate()

            plt.autoscale(enable=True, axis='both', tight=False)    

            plt.savefig(f"remorder/stream_db/indicator/{symbol}.png", dpi = 50)

            plt.clf()
            plt.close()
    except:
        logging.info("chart has created.")
        pass

if __name__ =="__main__":
    Strategy = "Diviation_Long"
    plot_indicator(Strategy)