# Importing packages

import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import plotly.express as px
import plotly.graph_objects as go


# Pulling Data

start = dt.datetime(2019,1,1)
end = dt.datetime.now()

stocks = web.DataReader(['FB','AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT'],
                        'yahoo', start, end)

df = pd.read_csv('PRVU.csv', parse_dates=True, index_col=0)
df2 = pd.read_csv('UPPER.csv', parse_dates=True, index_col=0)

stocks_close = pd.DataFrame(web.DataReader(['FB','AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT'],
                                           'yahoo', start, end)['Close'])




# Gauge charts

gauge = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = int(df2['adjclose'].tail(1)),
    mode = "gauge+number+delta",
    title = {'text':"<b>UPPER DAY RANGE</b><br><span style='color: gray; font-size:0.8em'>U.S. $</span>", 'font': {"size": 20}},
    delta = {'reference': int(df2['adjclose'].iloc[-2])},
    gauge = {
             'axis': {'range': [None, 300]},
             'steps' : [
                 {'range': [0, 200], 'color': "lightgray"},
                 {'range': [200, 300], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 276}}))

gauge.show()