import pandas as pd
from plotly.subplots import make_subplots

stockticker='UPPER'

LOOKUP_DAY=3

df1 = pd.read_csv(f'{stockticker}.csv', parse_dates=True, index_col=0)
#df2 = pd.read_csv(f'{stockticker}_machinelearn.csv', parse_dates=True, index_col=0)
df2 = pd.read_csv(f'C:/Users/NTC/PycharmProjects/stockpython/venv/LSTM/trained-results/{stockticker}_trained.csv', parse_dates=True, index_col=0)


#Left_join = pd.merge(df1, df2 ,how ='left')
Left_join = pd.concat([df1, df2['ichiconversionline_3']], axis=1)
Left_join.to_csv(f'{stockticker}.csv')


print(Left_join)