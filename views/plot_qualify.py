import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent  
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_config")

import matplotlib.pyplot as plt
import pandas as pd
from pandas import Timestamp # Don't remove
import numpy as np
import datetime, logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s : %(message)s")


def qualify_data(df, i):

    Ticker          = df['Ticker'][i]
    strategy        = df['strategy'][i]
    days            = df['days'][i]
    start           = df['start'][i]
    end             = df['end'][i]
    Core            = df['Core'][i]
    TR              = df['TR'][i]
    ATR             = df['ATR'][i]
    Trend           = df['Trend'][i]
    ResultAsset     = df['ResultAsset'][i]
    SampleSize      = df['SampleSize'][i]
    # Win_Ratio       = df['Win_Ratio'][i]
    # avgProfit       = df['avgProfit'][i]
    # avgLoss         = df['avgLoss'][i]
    # maxProfit       = df['maxProfit'][i]
    # maxLoss         = df['maxLoss'][i]
    unfinished_profit = df['unfinished_profit'][i]
    NET_PROFIT       = df['NET_PROFIT'][i]
    LatentLoss      = df['LatentLoss'][i]
    # EntryTimes      = df['EntryTimes'][i]
    ExitTimes       = df['ExitTimes'][i]

    # NET_PROFIT_001を{eval}を使ってstringからlistにしている。次に{map}でリスト内のデータをすべて1/100する関数を適応させる。結果がmapオブジェクトの型で返されるのでlistに戻している。
    #if __name__ == "__main__": 

    NET_PROFIT_001       = list(map(lambda x: x * 0.01, eval(NET_PROFIT)))
    NET_PROFIT           = list(eval(NET_PROFIT))

    LatentLoss_001       = list(map(lambda x: x * 0.01, eval(LatentLoss)))
    LatentLoss           = list(eval(LatentLoss))

    ExitTimes           = eval(ExitTimes)
    #Long_or_Short       = eval(Long_or_Short)

    # else:
    #     NET_PROFIT_001       = list(map(lambda x: x * 0.01, NET_PROFIT))
    #     NET_PROFIT           = list(NET_PROFIT)

    #     LatentLoss_001       = list(map(lambda x: x * 0.01, LatentLoss))
    #     LatentLoss           = list(LatentLoss)

    ExitTimes.insert(0, start) 
    list_NetP   = [0]
    list_asset  = [100]
    list_LatentLoss = [0]
    list_worst  = [100]
    list_trades = [0]
    #list_side   = ["None"]
    
    #profit = NET_PROFIT_001
    trades = len(NET_PROFIT_001)
    
    for trade, profit, result, bad, loss in zip(range(1,trades+1), NET_PROFIT_001, NET_PROFIT, LatentLoss_001, LatentLoss):

        asset = list_asset[-1]*(1 + profit)
        worst = list_asset[-1]*(1 + bad)

        list_asset  = np.append(list_asset,  asset)
        list_worst  = np.append(list_worst, worst)

        list_trades = np.append(list_trades, trade)
        #list_side   = np.append(list_side,   side)
        list_NetP   = np.append(list_NetP,   result)
        list_LatentLoss = np.append(list_LatentLoss, loss)

    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')

    Long_color = dict(facecolor="#2b6eff",
                edgecolor="#2b6eff",
                alpha=0.5,
                linewidth=2,
                linestyle="-")
    Short_color = dict(facecolor="#ff61ca",
                edgecolor="#ff61ca",
                alpha=0.5,
                linewidth=2,
                linestyle="-")
    LatenLoss_color = dict(facecolor="#420303",
                edgecolor="#420303",
                alpha=0.0,
                linewidth=2,
                linestyle="-")
    text_info = f"\n\
            SampleSize:   {SampleSize} tades\n\
            ResultAsset:  $ {round(ResultAsset,1)}\n\
            unfinished:    {round(unfinished_profit,1)} %\n\
            \n\
            Core:         {round(Core,1)}\n\
            TR:          {round(TR,1)}\n\
            ATR:          {round(ATR,1)}\n\
            Trend:         {round(Trend,1)}\n"

    return Ticker, strategy, days, ExitTimes, list_NetP, list_LatentLoss, list_asset,\
        list_worst, list_trades, now, Long_color, Short_color, LatenLoss_color, text_info


def plot_qualify(df, exportName_img):

    row_count, col_count = df.shape    

    ncol = 1
    nrow = int(np.ceil(row_count/ncol))

    print(f"ncol = {ncol}, nrow = {nrow}")
    plt.figure(figsize=(30,160))

    for iter, (row) in enumerate(df.iterrows()):
        
        ax = plt.subplot2grid((nrow, ncol), (iter//ncol, iter%ncol))

        Ticker, strategy, days, ExitTimes, list_NetP, list_LatentLoss, list_asset,\
        list_worst, list_trades, now, Long_color, Short_color, LatenLoss_color, text_info\
        = qualify_data(df, iter)

        ax.plot(list_trades, list_asset, marker='o', label="Asset", color='black')
        ax.plot(list_trades, list_worst, marker='o', label="Worst", color='red')
        #ax.axhline(y=200, xmin=0, xmax=1, linestyle="dashed", color = "gray")
        ax.set_xticks(range(len(ExitTimes)), ExitTimes)   
        ax.legend(loc = 'lower right') 

        for i in range(len(ExitTimes)):
            if "Long" in strategy:
                ax.text(list_trades[i], list_asset[i], f" #{list_trades[i]}, {(list_NetP[i])}%", bbox=Long_color)
            if "Short" in strategy:
                ax.text(list_trades[i], list_asset[i], f" #{list_trades[i]}, {(list_NetP[i])}%", bbox=Short_color)
            if list_trades[i] != 0:
                ax.text(list_trades[i], list_worst[i], f"{list_LatentLoss[i]}%", bbox=LatenLoss_color)
                
        ax.text(0, 100, text_info)
        ax.set_title(Ticker)


    plt.gcf().autofmt_xdate()
    plt.autoscale(enable=True, axis='both', tight=False) 

    logging.info("Generating Chart Image...")
    plt.savefig(exportName_img)


if __name__ == "__main__": 


    exportName_img = f"{project_dir}/static/Diviation_Long_2022_1004_0313_Qualify.png"

    df = pd.read_csv(f"{project_dir}/static/Diviation_Long_2022_1004_0313_Qualify.csv")
    plot_qualify(df, exportName_img)
    logging.info("qualify image OK")

    # plot_indicator()
    # logging.info("indicator image OK")

    logging.info("All cahrt has created successfuly")
