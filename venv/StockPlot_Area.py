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


# Area chart

area_chart = px.area(df['adjclose'], title = 'PRAVU BANK SHARE PRICE (2013-2020)')
#area_chart = px.area(stocks_close.FB, title = 'FACEBOOK SHARE PRICE (2013-2020)')

area_chart.update_xaxes(title_text = 'Date')
area_chart.update_yaxes(title_text = 'PRAVU BANK Close Price', tickprefix = '$')
area_chart.update_layout(showlegend = False)

area_chart.show()

# Customized chart

c_area = px.area(df['adjclose'], title = 'PRAVU BANK SHARE PRICE (2013-2020)')

c_area.update_xaxes(
    title_text = 'Date',
    rangeslider_visible = True,
    rangeselector = dict(
        buttons = list([
            dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
            dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
            dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
            dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
            dict(step = 'all')])))

c_area.update_yaxes(title_text = 'PRAVU BANK Close Price', tickprefix = '$')
c_area.update_layout(showlegend = False,
    title = {
        'text': 'PRAVU BANK SHARE PRICE (2013-2020)',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

c_area.show()
