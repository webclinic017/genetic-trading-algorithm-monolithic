import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
from batch import screener, kline

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def run(df, Ticker, ActivationTime, CandleTimeFrame, drop_VolUSD, drop_NATR):

    fig = plt.figure(figsize = (20,12), facecolor='lightblue')
    show_range   = int(7*1440 /CandleTimeFrame)
    x = df['OpenTime'].tail(show_range)

    total_charts = 4

    ax1 = fig.add_subplot(total_charts, 1, 1)
    ax1.set_title(f'{Ticker}: {ActivationTime}', fontsize=18)
    y_NATR = df['Close'].tail(show_range)
    ax1.plot(x, y_NATR, marker='', color= "green", label="Close")
    ax1.grid(axis='both',linestyle='dotted', color='gray')
    ax1.set_ylabel('Close')
    ax1.legend(loc='upper left')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%D %H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=6))

    ax2 = fig.add_subplot(total_charts, 1, 2)
    y_NATR = df['VolRatio'].tail(show_range)
    ax2.plot(x, y_NATR, marker='', color= "red", label="VolRatio")
    ax2.axhline(y=0, xmin=0, xmax=1, linestyle="solid", color = "gray")
    ax2.axhline(y=100, xmin=0, xmax=1, linestyle="dashed", color = "gray")
    ax2.axhline(y=-100, xmin=0, xmax=1, linestyle="dashed", color = "gray")
    ax2.grid(axis='both',linestyle='dotted', color='gray')
    ax2.set_ylabel('VolRatio')
    ax2.legend(loc='upper left')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%D %H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=6))

    ax3 = fig.add_subplot(total_charts, 1, 3)
    y_VolUSD_SMA = df['VolUSD_SMA'].tail(show_range)
    ax3.plot(x, y_VolUSD_SMA, marker='', color= "purple", label="VolUSD_SMA")
    ax3.axhline(y=0, xmin=0, xmax=1, linestyle="solid", color = "gray")
    ax3.axhline(y=drop_VolUSD, xmin=0, xmax=1, linestyle="dashed", color = "gray")
    ax3.axhline(y=10000000, xmin=0, xmax=1, linestyle="dashed", color = "gray")        
    ax3.grid(axis='both',linestyle='dotted', color='gray')
    ax3.set_ylabel('VolUSD_SMA')
    ax3.legend(loc='upper left')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%D %H:%M'))
    ax3.xaxis.set_major_locator(mdates.HourLocator(interval=6))

    ax4 = fig.add_subplot(total_charts, 1, 4)
    y_NATR = df['NATR'].tail(show_range)
    ax4.plot(x, y_NATR, marker='', color= "green", label="NATR")
    ax4.axhline(y=0,         xmin=0, xmax=1, linestyle="solid", color = "gray")
    ax4.axhline(y=drop_NATR, xmin=0, xmax=1, linestyle="solid", color = "gray")
    ax4.axhline(y=10,        xmin=0, xmax=1, linestyle="dashed", color = "gray")
    ax4.grid(axis='both',linestyle='dotted', color='gray')
    ax4.set_ylabel('NATR')
    ax4.legend(loc='upper left')
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%D %H:%M'))
    ax4.xaxis.set_major_locator(mdates.HourLocator(interval=6))

    plt.gcf().autofmt_xdate()
    plt.savefig(f"./backtest/data/SCREEN/{ActivationTime}/{Ticker}", dpi=50)
    plt.close()

    print(f"Ploted Screener Chart. {Ticker}")





if __name__ == "__main__": 

    Ticker = "BTCUSDT"
    ActivationTime = "000000000000"

    fetch_days = 33
    CandleTimeFrame = 60

    drop_VolUSD = 0
    drop_NATR = 0
    
    run(df, Ticker, ActivationTime, CandleTimeFrame, drop_VolUSD, drop_NATR)


    #---------------------------------------- PLOT --------------------------------------------------
    """
    list_passed_Ticker = passed_df['Ticker'].tolist()
    print(list_passed_Ticker)

    for Ticker in list_passed_Ticker:

        df = kline.fetch(Ticker, fetch_days, CandleTimeFrame)
        df = create_df(df)

        plot_screen.run(df, Ticker, ActivationTime, CandleTimeFrame, drop_VolUSD, drop_NATR)
    """

