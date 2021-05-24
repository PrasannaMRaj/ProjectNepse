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


df = pd.read_csv('NEPSE_index.csv', parse_dates=True, index_col=0)

stocks_close = pd.DataFrame(web.DataReader(['FB','AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT'],
                                           'yahoo', start, end)['Close'])



# Simple candlestick

candlestick = go.Figure(data = [go.Candlestick(x = df['date'],
                                               open = df['open'],
                                               high = df['high'],
                                               low = df['low'],
                                               close = df['adjclose'])])

candlestick.update_layout(xaxis_rangeslider_visible = False, title = 'NEPSE SHARE PRICE (2013-2020)')
candlestick.update_xaxes(title_text = 'Date')
candlestick.update_yaxes(title_text = 'NEPSE Close Price', tickprefix = 'Rs.')

candlestick.show()

# Customized candlestick

c_candlestick = go.Figure(data = [go.Candlestick(x = df['date'],
                                               open = df['open'],
                                               high = df['high'],
                                               low = df['low'],
                                               close = df['adjclose'])])

c_candlestick.update_xaxes(
    title_text = 'Date',
    rangeslider_visible = True,
    rangeselector = dict(
        buttons = list([
            dict(count = 1, label = '1D', step = 'day', stepmode = 'backward'),
            dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
            dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
            dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
            dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
            dict(step = 'all')])))

c_candlestick.update_layout(
    title = {
        'text': 'NEPSE SHARE PRICE (2013-2020)',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        })
c_candlestick.update_yaxes(title_text = 'NEPSE Close Price', tickprefix = 'Rs.')


#add bollinger data
c_candlestick.add_trace(
    go.Scatter(
        x= df['date'],
        y=df['volatility_bbl'],fillcolor='blue'

    ))

c_candlestick.add_trace(
    go.Scatter(
        x= df['date'],
        y=df['volatility_bbh'],fillcolor='blue'

    ))

c_candlestick.add_trace(
    go.Scatter(
        x= df['date'],
        y=df['volatility_bbm'],fillcolor='red'

    ))

c_candlestick.show()


#CANDLESTICK ENDS HERE