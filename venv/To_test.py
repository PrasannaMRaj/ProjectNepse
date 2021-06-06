import pandas as pd
import numpy as np


def implement_bb_strategy(df_signal,stockticker):


    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0
    print(len(df_signal))

    for i in range(len(df_signal)-1):
        i=i+1
        #print (i)
        if df_signal['adjclose'][i - 1] > df_signal['volatility_bbl_3'][i - 1] and df_signal['adjclose'][i] < df_signal['volatility_bbl_3'][i]:
            if signal != 100:
                buy_price.append(df_signal['adjclose'][i])
                sell_price.append(np.nan)
                signal = 100
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif df_signal['adjclose'][i - 1] < df_signal['volatility_bbh_3'][i - 1] and df_signal['adjclose'][i] > df_signal['volatility_bbh_3'][i]:
            if signal != -100:
                buy_price.append(np.nan)
                sell_price.append(df_signal['adjclose'][i])
                signal = -100
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)

    return buy_price, sell_price, bb_signal


stockticker="UPPER"
df_signal = pd.read_csv(f'{stockticker}.csv', parse_dates=True, index_col=0)
df_sig_value=pd.DataFrame()
buy,sell,df_sig_value['signal']=implement_bb_strategy(df_signal,stockticker)


Left_join = pd.concat([df_signal, df_sig_value], axis=1)
Left_join.to_csv(f'{stockticker}.csv')