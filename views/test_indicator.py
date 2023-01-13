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
from strategy import Devi
from batch import module as bt_module
import pandas_ta as ta
logging.basicConfig(level=logging.INFO,format="%(asctime)s : %(message)s")

# TODO: This system going to be ploted by Chart.js (bankof3v.com)

def plot_indicator(Strategy):

    os.makedirs(f"{working_dir}/static/TEMP/", exist_ok=True)

    df_param = pd.read_csv(f"/home/viceversa/Dropbox/bankof3v/static/TEST/DeviL/202211110706/BTCUSDT.csv")

    symbol  = df_param["Symbol"][0] 
    ATR     = df_param["ATR"][0] 
    TR      = df_param["TR"][0] 
    CORE    = df_param["Core"][0] 
    TREND   = df_param["Trend"][0] 

    print(f"target -> {symbol}")

    df_kline = bt_module.kline(symbol, 2, 1)
    df_kline = Devi.create_df(df_kline, ATR, CORE, TR, TREND, trading=True)
    
    show_range = int(100)

    x_opentime = df_kline['OpenTime'].tail(show_range)
    y_close = df_kline['Close'].tail(show_range)
    y_trend = df_kline['TREND'].tail(show_range)
    y_upper = df_kline['Upper'].tail(show_range)
    y_lower = df_kline['Lower'].tail(show_range)
    y_core  = df_kline['CORE'].tail(show_range)

    fig = plt.figure(figsize=(25, 7), dpi=72)
    fig.suptitle(f'test indi', fontsize=13)

    ax = fig.add_subplot(111)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    ax.plot(x_opentime,y_close, marker="o", label="close")
    ax.plot(x_opentime,y_trend, marker="o", label="trend")
    ax.plot(x_opentime,y_upper, marker="o", label="upper")
    ax.plot(x_opentime,y_lower, marker="o", label="lower")
    ax.plot(x_opentime,y_core, marker="o", label="core")

    ax.legend(loc = 'lower left') 

    ax.set_title(symbol, fontsize=10)

    plt.gcf().autofmt_xdate()

    plt.autoscale(enable=True, axis='both', tight=False)    

    plt.savefig(f"{Strategy}_{symbol}.png", dpi = 72)

    # plt.clf()
    # plt.close()


if __name__ =="__main__":
    Strategy = "DeviL"
    plot_indicator(Strategy)