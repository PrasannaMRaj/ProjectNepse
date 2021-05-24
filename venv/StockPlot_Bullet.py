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
df3 = pd.read_csv('SHIVM.csv', parse_dates=True, index_col=0)

stocks_close = pd.DataFrame(web.DataReader(['FB','AMZN', 'AAPL', 'NFLX', 'GOOGL', 'MSFT'],
                                           'yahoo', start, end)['Close'])


print(int(df['adjclose'].tail(1)))
print(int(df['adjclose'].iloc[-2]))
# Basic bullet chart

bullet_chart = go.Figure(go.Indicator(
    mode = "number+gauge+delta",
    gauge = {'shape': "bullet",
             'axis': {'range': [None, 600]}},
    value = int(df['adjclose'].tail(1)),
    delta = {'reference': int(df['adjclose'].iloc[-2])},
    domain = {'x': [0, 1],
              'y': [0, 1]},
    title = {'text':"<b>PRAVU BANK<br>DAY<br>RANGE</b><br><span style='color: gray; font-size:0.8em'>U.S. $</span>",
             'font': {"size": 16}}))

bullet_chart.update_layout(height = 250)

bullet_chart.show()

# Customized bullet chart

c_bullet = go.Figure()

c_bullet.add_trace(go.Indicator(
    mode = "number+gauge+delta",
    value = int(df['adjclose'].tail(1)),
    delta = {'reference': int(df['adjclose'].iloc[-2])},
    domain = {'x': [0.25, 1],
              'y': [0.08, 0.25]},
    title = {'text':"<b>PRAVU BANK DAY<br>RANGE</b><br><span style='color: gray; font-size:0.8em'>U.S. $</span>",
             'font': {"size": 14}},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 550]},
        'threshold': {
            'line': {'color': "Red", 'width': 2},
            'thickness': 0.75,
            'value': 505},
        'steps': [
            {'range': [0, 350], 'color': "gray"},
            {'range': [350, 550], 'color': "lightgray"}],
        'bar': {'color': 'black'}}))

c_bullet.add_trace(go.Indicator(
    mode = "number+gauge+delta",
    value = int(df2['adjclose'].tail(1)),
    delta = {'reference': int(df2['adjclose'].iloc[-2])},
    domain = {'x': [0.25, 1],
              'y': [0.4, 0.6]},
    title = {'text':"<b>UPPER DAY<br>RANGE</b><br><span style='color: gray; font-size:0.8em'>U.S. $</span>",
             'font': {"size": 14}},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 1800]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value': 1681},
        'steps': [
            {'range': [0, 1300], 'color': "gray"},
            {'range': [1300, 1800], 'color': "lightgray"}],
        'bar': {'color': 'black'}}))

c_bullet.add_trace(go.Indicator(
    mode = "number+gauge+delta",
    value = int(df3['adjclose'].tail(1)),
    delta = {'reference': int(df3['adjclose'].iloc[-2])},
    domain = {'x': [0.25, 1],
              'y': [0.7, 0.9]},
    title = {'text':"<b>SHIVM DAY<br>RANGE</b><br><span style='color: gray; font-size:0.8em'>U.S. $</span>",
             'font': {"size": 14}},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 250]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value': 208},
        'steps': [
            {'range': [0, 150], 'color': "gray"},
            {'range': [150, 250], 'color': "lightgray"}],
        'bar': {'color': "black"}}))

c_bullet.update_layout(height = 400 , margin = {'t':0, 'b':0, 'l':0})

c_bullet.show()


