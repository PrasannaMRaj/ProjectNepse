import pandas as pd
from plotly.subplots import make_subplots



stock_options=['PRVU','UPPER','SHIVM','NEPSE_index']
dataf=pd.DataFrame()

for i in stock_options:
    df1 = pd.read_csv(f'{i}.csv', parse_dates=True, index_col=0)
    df1 = df1.set_index('date')
    df1.index = pd.to_datetime(df1.index)
    df1_date_unavailable = pd.date_range(start=df1.index[0],
                                         end=df1.index[len(df1.index) - 1]).difference(df1.index)
    valuedate = df1_date_unavailable.strftime('20%y-%m-%d').tolist()
    dataf2=pd.DataFrame()
    dataf2[i]=valuedate

    dataf=pd.concat([dataf,dataf2],ignore_index=True)

print(dataf['NEPSE_index'].dropna(axis=0))
#dataf.to_csv('datframetest.csv', index=True, encoding="utf-8")