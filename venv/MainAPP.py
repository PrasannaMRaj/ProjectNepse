import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import dash_daq as daq

paper_bg_color = "#f7f1f3"
plot_bg_color = "#faf7f7"
style_for_Sig_dropdown = {'width': '10%','display': 'inline-block','padding-left':'45%','color':'black','font-size':'15px', 'optionHeight':'16px','text-align':'left'}
style_for_dropdown = {'width': '20%','display': 'inline-block','padding-left':'20px','color':'black','font-size':'14px', 'optionHeight':'16px','text-align':'left'}
#style_for_label = {'padding-left':'10px','color':'#b06969','font-size':'14px', 'text-align':'left','justify-content':'left'}
style_for_heading = {'font-size':'26px','color':'#165f98','text-align':'center','margin-top':'5px','margin-left':'20px','margin-bottom':'2px'}
style_for_sub_heading = {'font-size':'18px','color':'#165f98','text-align':'center','margin-top':'5px','margin-left':'20px'}
#style_for_graph = {'font-size':'22px','color':'#165f98','text-align':'center','margin-top':'5px','margin-left':'5px'}
picker_style = {'float': 'left', 'margin': 'auto','display': 'inline-block','padding-left':'10%'}

#stock_options=['PRVU','UPPER','SHIVM','NEPSE_index']
stock_options=['PRVU','UPPER','NEPSE_index','DDBL','CHCL','SHIVM']
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


indicator_options=['ema200','bollinger','keltner_channel','ichiconversionline','volatility_atr','adjclose_3']
ml_indicator_options=['BOLLINGER','KELTNER_CHANNEL','volatility_kcw_3','ichiconversionline_3']
subindicator_options=['macd','rsi','volatility_atr']
signal_indicator_options=['signal']

app = dash.Dash()

app.layout = html.Div([
    html.H2("Stock Report",style=style_for_heading),
    html.Div(
        [
            html.Label(["Choose_Stock"],style=style_for_dropdown),
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
            html.Label(["INDICATOR"],style=style_for_dropdown),
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
    html.Div([
            html.Label(["SUBINDICATOR"],style=style_for_dropdown),
            dcc.Dropdown(
                id="SUBINDICATOR",
                options=[{
                    'label': k,
                    'value': k
                } for k in subindicator_options],
                value='macd'),
        ],style=style_for_dropdown,
        #style={'width': '15%','height': '20%',
        #       'display': 'inline-block',
        #       'backgroundColor' :'#202228'}
    ),
    html.Div([
        html.Label(["ML_INDICATOR"],style=style_for_dropdown),
        dcc.Dropdown(
            id="ML_INDICATOR",
            options=[{
                'label': l,
                'value': l
            } for l in ml_indicator_options],
            value='BOLLINGER'),
    ], style=style_for_dropdown,
        # style={'width': '15%','height': '20%',
        #       'display': 'inline-block',
        #       'backgroundColor' :'#202228'}
    ),
    html.Hr(),
    html.Div([
        html.Label(["SIGNAL"],style=style_for_dropdown),
        dcc.Dropdown(
            id="SIGNAL_INDICATOR",
            options=[{
                'label': m,
                'value': m
            } for m in signal_indicator_options],
            value='signal'),
    ], style=style_for_Sig_dropdown,
        # style={'width': '15%','height': '20%',
        #       'display': 'inline-block',
        #       'backgroundColor' :'#202228'}
    ),

    html.Div([dcc.Graph(id='stock_graph',figure={'layout': {'height': 850}})],style={'height': '100%','width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    #dcc.Graph(id='stock_graph'),

    daq.ColorPicker(
        id='font', label='Font Color', size=180,
        style=picker_style, value=dict(hex='#119DFF')),
    daq.ColorPicker(
        id='title', label='Title Color', size=180,
        style=picker_style, value=dict(hex='#2A0203')),
    daq.ColorPicker(
        id='plot_backgr', label='PLOT Color', size=180,
        style=picker_style, value=dict(hex=plot_bg_color)),
    daq.ColorPicker(
        id='paper_backgr', label='Background Color', size=180,
        style=picker_style, value=dict(hex=paper_bg_color)),

    html.Br(),

    html.Div([dcc.Graph(id='fundamental_graph', figure={'layout': {'height': 500}})],
             style={'height': '100%', 'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),

],style={'height': '100%','backgroundColor' :paper_bg_color})##add6ff

@app.callback(
    dash.dependencies.Output('stock_graph', 'figure'),
    [dash.dependencies.Input('STOCK', 'value'),
     dash.dependencies.Input('INDICATOR', 'value'),
     dash.dependencies.Input('SUBINDICATOR', 'value'),
     dash.dependencies.Input('ML_INDICATOR', 'value'),
     dash.dependencies.Input('SIGNAL_INDICATOR', 'value'),
     dash.dependencies.Input("font", 'value'),
     dash.dependencies.Input("title", 'value'),
     dash.dependencies.Input("plot_backgr", 'value'),
     dash.dependencies.Input("paper_backgr", 'value') ])

def update_value(STOCK,INDICATOR,SUBINDICATOR,ML_INDICATOR,SIGNAL_INDICATOR,font_color, title_color,plot_color,bg_color):
    df = pd.read_csv(f'{STOCK}.csv', parse_dates=True, index_col=0)

    #df1_date = df
    df = df.set_index('date')
    #df.index = pd.to_datetime(df.index)
    #df1_date_unavailable = pd.date_range(start=df.index[0],
    #                                    end=df.index[len(df.index) - 1]).difference(df.index)

    #valuedate=df1_date_unavailable.strftime('20%y-%m-%d').tolist()


    # Customized candlestick
    c_candlestick= make_subplots(rows=4, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.05,row_heights=[300,75,75,75],subplot_titles=('','Volume','Machine Learned Signal','Indicator'))

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
                                           close=df['adjclose'],name="Candle",increasing_line_color= 'white', decreasing_line_color= 'black'), row=1, col=1)

    #c_candlestick = go.Figure(data=[go.Candlestick(x=df['date'],open=df['open'], high=df['high'], low=df['low'],close=df['adjclose'])])



    c_candlestick.update_xaxes(
        #use below rangebreaks code if rangeslector is needed. ELSE rangebreaks is too slow to load chart
        #rangebreaks= [dict(values=dataf[STOCK].dropna(axis=0))],# hide unavailable days date

        #title_text='Date',
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

    #c_candlestick.update_layout(xaxis={'showgrid': False},yaxis={'showgrid': False})
    #c_candlestick.update_yaxes(title_text=STOCK, tickprefix='Rs.')

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
                y=df['volatility_bbm'], fillcolor='green', line=dict(width=1), marker=dict(color='yellow'),name="Bollinger middle"

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_bbh'], fillcolor='green', line=dict(width=2), marker=dict(color='blue'),name="Bollinger high"

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_bbl'], fillcolor='green', line=dict(width=2), marker=dict(color='blue'),name="Bollinger low"

            ), row=1, col=1)
    elif (INDICATOR == 'keltner_channel'):  # ichibaseline,ichiconversionline
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_kch'], line=dict(width=1), marker=dict(color='blue'),name="KELTNER high"

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_kcl'], line=dict(width=1), marker=dict(color='blue'),name="KELTNER low"

            ), row=1, col=1)
    else:
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df[INDICATOR], fillcolor='green', line=dict(width=2), marker=dict(color='blue'),name=INDICATOR

            ), row=1, col=1)


    #ML_indicators
    if(ML_INDICATOR=='BOLLINGER'):
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_bbm_3'], fillcolor='green', line=dict(width=1), marker=dict(color='brown'),name="ML_BB_MIDDLE"

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_bbh_3'], fillcolor='green', line=dict(width=2), marker=dict(color='red'),name="ML_BB_HIGH"

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_bbl_3'], fillcolor='green', line=dict(width=2), marker=dict(color='red'),name="ML_BB_LOW"

            ), row=1, col=1)
    elif(ML_INDICATOR=='KELTNER_CHANNEL'):   #ichibaseline,ichiconversionline
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_kch_3'], line=dict(width=1), marker=dict(color='red'),name="ML_KCH_HIGH"

            ), row=1, col=1)

        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df['volatility_kcl_3'],  line=dict(width=1), marker=dict(color='red'),name="ML_KCH_LOW"

            ), row=1, col=1)
    else:
        c_candlestick.add_trace(
            go.Scatter(
                x=df.index,
                y=df[ML_INDICATOR], fillcolor='green', line=dict(width=2), marker=dict(color='green'),name=ML_INDICATOR

            ), row=1, col=1)



    #c_candlestick.add_trace(go.Bar(x=df['date'],y=df['volume'],name='Volume',marker=dict( color='brown')), secondary_y=False,row=2, col=1)
    c_candlestick.add_trace(go.Bar(x=df.index, y=df['volume'], name='Volume', marker=dict(color='black')), row=2, col=1)
    c_candlestick.add_trace(go.Scatter(x=df.index, y=df[SIGNAL_INDICATOR],name=SIGNAL_INDICATOR, line=dict(width=2),
                                       marker=dict(color='ORANGE')), row=3, col=1)
    c_candlestick.add_trace(go.Scatter(x=df.index,y=df[SUBINDICATOR],name=SUBINDICATOR, fillcolor='green', line=dict(width=2), marker=dict(color='YELLOW') ), row=4, col=1)

    c_candlestick.update_layout(xaxis={'showgrid': False}, yaxis={'showgrid': False},font_color=font_color['hex'],title_font_color=title_color['hex'],plot_bgcolor=plot_color['hex'],paper_bgcolor=bg_color['hex'])

    c_candlestick.update_yaxes(title_text=STOCK, tickprefix='Rs.',gridcolor=plot_bg_color)
    return c_candlestick


#Fundamental Graph
@app.callback(
    dash.dependencies.Output('fundamental_graph', 'figure'),
    [dash.dependencies.Input('STOCK', 'value')])

def update_fundamental(STOCK):
    c_fundamental = make_subplots(rows=1, cols=2,
                                  shared_xaxes=True,
                                  horizontal_spacing=0.2,column_widths=[100,100])


    c_fundamental.add_trace(go.Bar(x=[100,200],y=[5,10]),row=1, col=1)
    c_fundamental.add_trace(go.Bar(x=[200, 100], y=[2, 3]), row=1, col=2)
    #c_fundamental.add_trace(go.Pie(values=[10,4,1]), row=1, col=2)
    return c_fundamental





if __name__ == "__main__":
    app.run_server(debug=True)




