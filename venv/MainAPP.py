import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots

paper_bg_color = "#f7f1f3"
plot_bg_color = "#faf7f7"
style_for_dropdown = {'width': '20%','display': 'inline-block','padding-left':'15px','color':'black','font-size':'14px', 'optionHeight':'16px','text-align':'left'}
#style_for_label = {'padding-left':'10px','color':'#b06969','font-size':'14px', 'text-align':'left','justify-content':'left'}
style_for_heading = {'font-size':'26px','color':'#165f98','text-align':'center','margin-top':'5px','margin-left':'20px','margin-bottom':'2px'}
style_for_sub_heading = {'font-size':'18px','color':'#165f98','text-align':'center','margin-top':'5px','margin-left':'20px'}
#style_for_graph = {'font-size':'22px','color':'#165f98','text-align':'center','margin-top':'5px','margin-left':'5px'}


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


indicator_options=['ema200','bollinger','ichimoku_cloud','volatility_atr','macd','rsi']

app = dash.Dash()

app.layout = html.Div([
    html.H2("Stock Report",style=style_for_heading),
    html.Div(
        [
            dcc.Dropdown(
                id="STOCK",
                options=[{
                    'label': i,
                    'value': i
                } for i in stock_options],
                value='PRVU'),
        ],style=style_for_dropdown,
        #style={'width': '20%','height': '20%',
        #       'display': 'inline-block',       'backgroundColor' :'#c6bcb6','padding': '200 100'}
               ),
    html.Div([
            dcc.Dropdown(
                id="INDICATOR",
                options=[{
                    'label': j,
                    'value': j
                } for j in indicator_options],
                value='ema200'),
        ],style=style_for_dropdown,
        #style={'width': '15%','height': '20%',
        #       'display': 'inline-block',
        #       'backgroundColor' :'#202228'}
    ),

    html.Div([dcc.Graph(id='stock_graph',figure={'layout': {'height': 700}})],style={'height': '100%','width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    #dcc.Graph(id='stock_graph'),

],style={'height': '100%','backgroundColor' :paper_bg_color})##add6ff

@app.callback(
    dash.dependencies.Output('stock_graph', 'figure'),
    [dash.dependencies.Input('STOCK', 'value'),
     dash.dependencies.Input('INDICATOR', 'value')])

def update_value(STOCK,INDICATOR):
    df = pd.read_csv(f'{STOCK}.csv', parse_dates=True, index_col=0)

    #df1_date = df
    df = df.set_index('date')
    #df.index = pd.to_datetime(df.index)
    #df1_date_unavailable = pd.date_range(start=df.index[0],
    #                                    end=df.index[len(df.index) - 1]).difference(df.index)

    #valuedate=df1_date_unavailable.strftime('20%y-%m-%d').tolist()


    # Customized candlestick
    c_candlestick= make_subplots(rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1,row_heights=[200,50])

    #c_candlestick = make_subplots(specs=[[{"secondary_y": True}]])

    #c_candlestick.add_trace(go.Candlestick(x=df['date'],
    #                                               open=df['open'],
    #                                               high=df['high'],
    #                                               low=df['low'],
    #                                               close=df['adjclose']),secondary_y=True)

    c_candlestick.add_trace(go.Candlestick(x=df.index,
                                           open=df['open'],
                                           high=df['high'],
                                           low=df['low'],
                                           close=df['adjclose']), row=1, col=1)

    #c_candlestick = go.Figure(data=[go.Candlestick(x=df['date'],open=df['open'], high=df['high'], low=df['low'],close=df['adjclose'])])



    c_candlestick.update_xaxes(
        #use below rangebreaks code if rangeslector is needed. ELSE rangebreaks is too slow to load chart
        #rangebreaks= [dict(values=dataf[STOCK].dropna(axis=0))],# hide unavailable days date

        title_text='Date',
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1D', step='day', stepmode='backward'),
                dict(count=1, label='1M', step='month', stepmode='backward'),
                dict(count=6, label='6M', step='month', stepmode='backward'),
                dict(count=1, label='YTD', step='year', stepmode='todate'),
                dict(count=1, label='1Y', step='year', stepmode='backward'),
                dict(step='all')])))

    c_candlestick.update_layout(

        title={
            'text': STOCK,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },plot_bgcolor='darkslategray',paper_bgcolor="LightSteelBlue",xaxis = dict(type="category"))#'#edc9ff' #darkslategray LightSteelBlue

    c_candlestick.update_layout(xaxis={'showgrid': False},yaxis={'showgrid': False})
    c_candlestick.update_yaxes(title_text=STOCK, tickprefix='Rs.')




    #c_candlestick.add_trace(
    #    go.Scatter(
    #        x=df['date'],
    #        y=df[INDICATOR], fillcolor='green',line = dict( width = 2 ),marker=dict(color='blue'),
#
 #       ),secondary_y=True ,row=2, col=1)
    #Bollinger
    if(INDICATOR=='bollinger'):
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_bbm'], fillcolor='green', line=dict(width=1), marker=dict(color='yellow'),

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_bbh'], fillcolor='green', line=dict(width=2), marker=dict(color='blue'),

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_bbl'], fillcolor='green', line=dict(width=2), marker=dict(color='blue'),

            ), row=1, col=1)
    elif(INDICATOR=='ichimoku_cloud'):   #ichibaseline,ichiconversionline
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['ichilinea'], line=dict(width=1), marker=dict(color='red'),

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['ichilineb'],  line=dict(width=1), marker=dict(color='blue'),

            ), row=1, col=1)
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['ichibaseline'], line=dict(width=1), marker=dict(color='green'),

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['ichiconversionline'], line=dict(width=1), marker=dict(color='yellow'),

            ), row=1, col=1)

    else:
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df[INDICATOR], fillcolor='green', line=dict(width=2), marker=dict(color='blue'),

            ), row=1, col=1)

    #c_candlestick.add_trace(go.Bar(x=df['date'],y=df['volume'],name='Volume',marker=dict( color='brown')), secondary_y=False,row=2, col=1)
    c_candlestick.add_trace(go.Bar(x=df.index, y=df['volume'], name='Volume', marker=dict(color='black')), row=2, col=1)
    return c_candlestick



if __name__ == "__main__":
    app.run_server(debug=True)




