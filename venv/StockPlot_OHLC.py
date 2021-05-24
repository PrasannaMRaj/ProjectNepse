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

stocks_close = pd.DataFrame(web.DataReader(['FB','AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT'],
                                           'yahoo', start, end)['Close'])

# Simple OHLC chart

ohlc = go.Figure(data = [go.Ohlc(x = df.index,
                                               open = df['open'],
                                               high = df['high'],
                                               low = df['low'],
                                               close = df['adjclose'])])

ohlc.update_layout(xaxis_rangeslider_visible = False, title = 'APPLE SHARE PRICE (2013-2020)')
ohlc.update_xaxes(title_text = 'Date')
ohlc.update_yaxes(title_text = 'AAPL Close Price', tickprefix = '$')

ohlc.show()

# Customized OHLC

c_ohlc = go.Figure(data = [go.Ohlc(x = df.index,
                                               open = df['open'],
                                               high = df['high'],
                                               low = df['low'],
                                               close = df['adjclose'])])

c_ohlc.update_xaxes(
    title_text = 'Date',
    rangeslider_visible = True,
    rangeselector = dict(
        buttons = list([
            dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
            dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
            dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
            dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
            dict(step = 'all')])))

c_ohlc.update_layout(
    title = {
        'text': 'APPLE SHARE PRICE (2013-2020)',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
c_ohlc.update_yaxes(title_text = 'AAPL Close Price', tickprefix = '$')

c_ohlc.show()

#ohlc CHART ENDS HERE