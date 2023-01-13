import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/tools")

import sys, logging, sqlite3, pathlib
from tools import report
import pandas as pd

from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")


# POSITION
import ast, datetime

def func_datatime_data(account_data):
    data_time = account_data[1]
    data_time = datetime.datetime.fromtimestamp(data_time)
    data_time = data_time.strftime('%Y/%m/%d %H:%M:%S')
    return data_time


def func_position_data(account_data):

    position_data = account_data[3]
    position_data = ast.literal_eval(position_data)

    list_entryPrice = []
    list_isAutoAddMargin = []
    list_isolatedMargin = []
    list_isolatedWallet = []
    list_leverage = []
    list_liquidationPrice = []
    list_marginType = []
    list_markPrice = []
    list_maxNotionalValue = []
    list_notional = []
    list_positionAmt = []
    list_positionSide = []
    list_positionSymbol = []
    list_unRealizedProfit = []
    list_updateTime = []

    for i in range(len(position_data)):
        # entryPrice      = float(position_data[i]["entryPrice"])
        # isAutoAddMargin = position_data[i]["isAutoAddMargin"]
        # isolatedMargin  = float(position_data[i]["isolatedMargin"])
        # isolatedWallet  = float(position_data[i]["isolatedWallet"])
        # leverage        = float(position_data[i]["leverage"])
        # liquidationPrice= float(position_data[i]["liquidationPrice"])
        # marginType      = position_data[i]["marginType"]
        # markPrice       = float(position_data[i]["markPrice"])
        # maxNotionalValue= float(position_data[i]["maxNotionalValue"])
        notional        = float(position_data[i]["notional"])
        # positionAmt     = float(position_data[i]["positionAmt"])
        positionSide    = position_data[i]["positionSide"]
        symbol          = position_data[i]["symbol"]
        unRealizedProfit= float(position_data[i]["unRealizedProfit"])
        # updateTime      = int(position_data[i]["updateTime"])

        # list_entryPrice.append(entryPrice)
        # list_isAutoAddMargin.append(isAutoAddMargin)
        # list_isolatedMargin.append(isolatedMargin)
        # list_isolatedWallet.append(isolatedWallet)
        # list_leverage.append(leverage)
        # list_liquidationPrice.append(liquidationPrice)
        # list_marginType.append(marginType)
        # list_markPrice.append(markPrice)
        # list_maxNotionalValue.append(maxNotionalValue)
        list_notional.append(notional)
        # list_positionAmt.append(positionAmt)
        list_positionSide.append(positionSide)
        list_positionSymbol.append(symbol)
        list_unRealizedProfit.append(unRealizedProfit)
        # list_updateTime.append(updateTime)

    # #_____________________________________________________________
    # # if short position, notional is  negative number. It can't be used for pie chart. 
    # # I'm changing all short position(negative) to positive.
    list_all_positive_notional = []
    for i_list_notional in list_notional:
        if i_list_notional < 0:
            i_list_notional = i_list_notional *-1
        list_all_positive_notional.append(i_list_notional)
    # #____________________________________________________________
    total_notional = 0
    for i_notional in list_all_positive_notional:
        total_notional += float(i_notional)
    # #_____________________________________________________________
    list_positionSymbolAndSide = [i+"_"+j for i, j in zip(list_positionSymbol, list_positionSide)]
    # #_____________________________________________________________
    total_LONG_notional = 0
    total_Short_notional = 0
    for i_positionSide, i_notional in zip(list_positionSide, list_all_positive_notional):
        if i_positionSide == "LONG":
            total_LONG_notional += i_notional
        if i_positionSide == "SHORT":
            total_Short_notional += i_notional
    # #_____________________________________________________________
    total_unRealizedProfitLoss = 0
    total_unRealized_ProfitONLY = 0
    total_unRealized_LossONLY_Positive = 0
    total_unRealized_LossONLY_Nagative = 0
    for i_unRealizedProfit in list_unRealizedProfit:
        total_unRealizedProfitLoss += i_unRealizedProfit
        if i_unRealizedProfit > 0:
            total_unRealized_ProfitONLY += i_unRealizedProfit
        else:
            total_unRealized_LossONLY_Positive += (i_unRealizedProfit*-1)
            total_unRealized_LossONLY_Nagative += i_unRealizedProfit
    

    return  list_entryPrice,        list_isAutoAddMargin,   list_isolatedMargin,\
            list_isolatedWallet,    list_leverage,          list_liquidationPrice,\
            list_marginType,        list_markPrice,         list_maxNotionalValue,\
            list_notional,          list_positionAmt,       list_positionSide, \
            list_positionSymbol,    list_unRealizedProfit,  list_updateTime, \
            total_notional,         list_all_positive_notional,   list_positionSymbolAndSide,\
            total_LONG_notional,    total_Short_notional,         total_unRealizedProfitLoss,\
            total_unRealized_ProfitONLY, total_unRealized_LossONLY_Positive, total_unRealized_LossONLY_Nagative

        # list_entryPrice = position_data[0]
        # list_isAutoAddMargin = position_data[1]
        # list_isolatedMargin = position_data[2]
        # list_isolatedWallet = position_data[3]
        # list_leverage = position_data[4]
        # list_liquidationPrice = position_data[5]
        # list_marginType = position_data[6]
        # list_markPrice = position_data[7]
        # list_maxNotionalValue = position_data[8]
        # list_notional = position_data[9]
        # list_positionAmt = position_data[10]
        # list_positionSide = position_data[11]
        # list_positionSymbol = position_data[12]
        # list_unRealizedProfit = position_data[13]
        # list_updateTime = position_data[14]
        # total_notional = position_data[15]
        # list_all_positive_notional = position_data[16]
        # list_positionSymbolAndSide = position_data[17]
        # total_LONG_notional = position_data[18]
        # total_Short_notional = position_data[19]
        # total_unRealizedProfitLoss = position_data[20]
        # total_unRealized_ProfitONLY = position_data[21]
        # total_unRealized_LossONLY_Positive = position_data[22]
        # total_unRealized_LossONLY_Nagative = position_data[23]


def func_balance_data(account_data):
    balance_data = account_data[2]
    balance_data = ast.literal_eval(balance_data)
    #__________________________________________________________________
    # Balance
    total_balance = 0
    total_withdrawable = 0

    list_asset = []
    list_balance = []
    list_withdrawAvailable = []
    list_updateTime = []

    for i in range(len(balance_data)):
        # accountAlias = balance_data[i]["accountAlias"]
        asset        = balance_data[i]["asset"]
        balance      = float(balance_data[i]["balance"])
        withdrawAvailable = float(balance_data[i]["withdrawAvailable"])
        updateTime   = int(balance_data[i]["updateTime"])

        if asset == "USDT" or asset == "BUSD":
            list_asset.append(asset)
            list_balance.append(balance)
            list_withdrawAvailable.append(withdrawAvailable)
            list_updateTime.append(updateTime)

        total_balance += balance
        total_withdrawable += withdrawAvailable
    #____________________________

    total_balance = 0
    for i in list_balance:
        total_balance += i

    total_withdrawAvailable = 0
    for i in list_withdrawAvailable:
        total_withdrawAvailable += i

    return  list_asset, list_balance, list_withdrawAvailable, \
            list_updateTime, total_balance, total_withdrawAvailable


def create_list(exchangeName, debug = False):
    try:
        singleRecordMin = 5
        lookbackDays = 3
        lookbackRangeMin = 1440*lookbackDays
        lookbackRangeBars = int(lookbackRangeMin/singleRecordMin)
        TargetAmountOfBars = 50
        DistanceOfBars = int(lookbackRangeBars/TargetAmountOfBars)

        connection = sqlite3.connect(f"{outside_dir}/bankof3v.db")
        c = connection.cursor()

        c.execute(f'SELECT * FROM account_{exchangeName} LIMIT {lookbackRangeMin}') 

        account_data = c.fetchall()

        connection.close()

        list_pick = []
        if debug == True:
            for i in reversed(range(0, 24 +1, 1)):
                list_pick.append(int(i))
        else:
            for i in reversed(range(0, lookbackRangeBars +1, DistanceOfBars)):
                list_pick.append(i)

        list_data_time = []
        list_total_balance = []
        list_total_withdrawAvailable = []
        list_total_notional = []
        list_total_LONG_notional = []
        list_total_SHORT_notional = []
        list_total_unRealizedProfitLoss = []
        list_total_unRealized_ProfitONLY = []
        list_total_unRealized_LossONLY_Nagative = []

        for i_pick in list_pick:
            try:
                data_time = func_datatime_data(account_data[i_pick])

                my_balance = func_balance_data(account_data[i_pick])
                total_balance = my_balance[4]
                total_withdrawAvailable = my_balance[5]

                my_position = func_position_data(account_data[i_pick])
                total_notional = my_position[15]
                total_LONG_notional = my_position[18]
                total_SHORT_notional = my_position[19]
                total_unRealizedProfitLoss = my_position[20]
                total_unRealized_LossONLY_Nagative = my_position[23]

                list_data_time.append(data_time)
                list_total_balance.append(total_balance)
                list_total_withdrawAvailable.append(total_withdrawAvailable)
                list_total_notional.append(total_notional)
                list_total_LONG_notional.append(total_LONG_notional)
                list_total_SHORT_notional.append(total_SHORT_notional)
                list_total_unRealizedProfitLoss.append(total_unRealizedProfitLoss)
                list_total_unRealized_ProfitONLY.append(list_total_unRealized_ProfitONLY)
                list_total_unRealized_LossONLY_Nagative.append(total_unRealized_LossONLY_Nagative)

            except:
                continue

        list_data_time = pd.to_datetime(list_data_time)

        return  list_data_time,\
                list_total_balance,\
                list_total_withdrawAvailable,\
                list_total_notional,\
                list_total_LONG_notional,\
                list_total_SHORT_notional,\
                list_total_unRealizedProfitLoss,\
                list_total_unRealized_ProfitONLY,\
                list_total_unRealized_LossONLY_Nagative


    except Exception as e:
        report.error(e, "Error database/account_history.py -> Error happend when I'm trying to get new account balance and position data.")
#_____________________________________
if __name__ == "__main__":
    exchangeName = "BINANCETESTNET"
    # exchangeName = "BINANCE"

    data = create_list(exchangeName, True)
    print(data[-1])
