
from bs4 import BeautifulSoup
import requests
import lxml.html as lh
import pandas as pd
import datetime
import pandas as pd
import csv
import json
import os
import time
from ta import add_all_ta_features

from ta.momentum import StochasticOscillator,StochRSIIndicator,RSIIndicator,WilliamsRIndicator
from ta.volatility import AverageTrueRange,BollingerBands,KeltnerChannel

from ta.trend import MACD
from ta.utils import dropna
from ta.trend import IchimokuIndicator,EMAIndicator


import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets

import sys


class ui_mainwindow(QtWidgets.QWidget):
        def setupui(self, mainwindow):
                mainwindow.resize(422, 255)
                self.centralwidget = QtWidgets.QWidget(mainwindow)

                self.pushbutton = QtWidgets.QPushButton(self.centralwidget)

                self.pushbutton.setGeometry(QtCore.QRect(160, 130, 93, 28))

                # for displaying confirmation message along with user's info.
                self.label = QtWidgets.QLabel(self.centralwidget)
                self.label.setGeometry(QtCore.QRect(170, 40, 201, 111))

                # keeping the text of label empty initially.
                self.label.setText("")

                mainwindow.setCentralWidget(self.centralwidget)
                self.retranslateui(mainwindow)
                QtCore.QMetaObject.connectSlotsByName(mainwindow)

        def retranslateui(self, mainwindow):
                _translate = QtCore.QCoreApplication.translate
                mainwindow.setWindowTitle(_translate("stockwebscrap", "stockwebscrap"))
                self.pushbutton.setText(_translate("stockwebscrap", "choosescrip"))
                self.pushbutton.clicked.connect(lambda: self.takeinputs())

        def takeinputs(self):
                scrip, done1 = QtWidgets.QInputDialog.getText(
                        self, 'price history', 'enter your scrip:')

                if done1 :
                        # showing confirmation message along
                        # with information provided by user.
                        self.label.setText(str(scrip) +'scrip web scrapping started !!! ')

                        try:
                                print(scrip)
                                start_requests(scrip)
                                self.label.setText(str(scrip)+'__' + ' web scrapping completed \nsuccessfully !!! ')
                        except:
                                self.label.setText('web scrapping failed. \n please choose another scrip ')

                        # hide the pushbutton after inputs provided by the use.
                        #self.pushbutton.settext(_translate("mainwindow", "choosescripagain"))
                        #self.pushbutton.hide()





#ticker='nica'
#for index add 'index' to last eg:nepse_index,banking_index

def start_requests(ticker):
        fromdate_origin = datetime.datetime(2000, 1, 1, 0, 0).timestamp()
        todate_origin = datetime.datetime(2021, int(time.strftime("%m")), int(time.strftime("%d")), 23, 59).timestamp()

        #print("fromdate: ",fromdate_origin)
        #print("to date: ", todate_origin)

        #url = "https://da.merolagani.com/handlers/technicalcharthandler.ashx"
        #payload = {"symbol": ticker, "resolution": "1d", "rangestartdate": fromdate_origin, "rangeenddate": todate_origin,
        #                   "isadjust":0 ,"currencycode": "nrs","type":"get_advanced_chart"}



        #url = "https://nepsealpha.com/trading/0/history"
        url = "https://backendtradingview.systemxlite.com/tradingviewsystemxlite/history"
        payload = {"symbol":ticker , "resolution":"1d" , "from":fromdate_origin , "to":todate_origin,"currencycode":"nrs"}


        page=requests.get(url,params=payload)
        #print(page)
        df = pd.DataFrame(page.json())
        #print(df)
        #df.columns=['date','adjclose','open','high','low','volume','other'] #for nepsealpha
        df.columns = ['status','date', 'adjclose', 'open', 'high', 'low', 'volume'] #for systemxlite


        #df['date'] = datetime.datetime.fromtimestamp(df['date']).strftime('%y-%m-%d')
        #df['date']= df['date'].date()
        #df['date'] = pd.to_datetime(df['date'].astype(int), unit='s')
        del df['status']
        #del df['date']
        df['date'] = df['date'].map(lambda val: datetime.datetime.fromtimestamp(val).strftime('20%y-%m-%d'))
        #<-df['date'] = pd.to_datetime(df['date'])
        #df['date'] = pd.to_datetime(df['date'], unit='s').dt.strftime('%y-%m-%d')
        timewindow=14
        df = df.replace(0, np.nan)


        #df['rsi'] = calcrsi(df['adjclose'],timewindow)

        rsi_data=RSIIndicator(close=df['adjclose'], window=timewindow)
        df['rsi']=rsi_data.rsi()

        stochosc_data = StochasticOscillator(high=df['high'], low=df['low'], close=df['adjclose'])
        df['stoch']=stochosc_data.stoch()
        #df['stochsignal']=stochosc_data.stoch_signal()

        stochrsi_data = StochRSIIndicator(close=df['adjclose'])
        df['momentum_stoch_rsi']=stochrsi_data.stochrsi()
        df['momentum_stoch_rsi_k'] = stochrsi_data.stochrsi_k()
        df['momentum_stoch_rsi_d'] = stochrsi_data.stochrsi_d()

        macd_data = MACD(window_slow=17, window_fast=8,close=df['adjclose'])
        df['macd']=macd_data.macd()
        df['macddiff'] = macd_data.macd_diff()

        volatility_data=AverageTrueRange(close=df['adjclose'], high=df['high'], low=df['low'], window=10)
        df['volatility_atr']=volatility_data.average_true_range()

        bollingerdata=BollingerBands(close=df['adjclose'], window=20)
        df['volatility_bbm']=bollingerdata.bollinger_mavg()
        df['volatility_bbl']=bollingerdata.bollinger_lband()
        df['volatility_bbh']=bollingerdata.bollinger_hband()
        df['volatility_bbw']=bollingerdata.bollinger_wband()

        keltner_data=KeltnerChannel(close=df['adjclose'], high=df['high'], low=df['low'], window=10)
        df['volatility_kch']=keltner_data.keltner_channel_hband()
        df['volatility_kcl']=keltner_data.keltner_channel_lband()
        df['volatility_kcw']=keltner_data.keltner_channel_wband()

        williamsr_data=WilliamsRIndicator(high=df['high'], low=df['low'], close=df['adjclose'], lbp=14)
        df['williamr']=williamsr_data.williams_r()

        ichimoku_data=IchimokuIndicator(high=df['high'], low=df['low'])
        df['ichibaseline']=ichimoku_data.ichimoku_base_line()
        df['ichiconversionline']=ichimoku_data.ichimoku_conversion_line()
        df['ichilinea']=ichimoku_data.ichimoku_b()
        df['ichilineb']=ichimoku_data.ichimoku_a()

        ema_data=EMAIndicator(close=df['adjclose'],window=200)
        df['ema200']=ema_data.ema_indicator()
        #alltechnical_data = add_all_ta_features(df, open="open", high="high", low="low", close="adjclose", volume="volume")

        df.to_csv(f'{ticker}.csv', index=True, encoding="utf-8")

def addtechnicalindicators(wholedata):
        #wholedata is the dataframe containing csv data of stock
        mom_data = add_all_ta_features(wholedata, open="open", high="high", low="low", close="adjclose", volume="volume")
        #print(mom_data.columns)

def addmomentumindicators(wholedata):
        #wholedata is the dataframe containing csv data of stock
        mom_data = add_all_ta_features(wholedata, open="open", high="high", low="low", close="adjclose", volume="volume")
        #print(mom_data.columns)


def calcrsi(data,time_window):
        diff = data.diff(1).dropna()  # diff in one field(one day)

        # this preservers dimensions off diff values
        up_chg = 0 * diff
        down_chg = 0 * diff

        # up change is equal to the positive difference, otherwise equal to zero
        up_chg[diff > 0] = diff[diff > 0]

        # down change is equal to negative deifference, otherwise equal to zero
        down_chg[diff < 0] = diff[diff < 0]

        # check pandas documentation for ewm
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.dataframe.ewm.html
        # values are related to exponential decay
        # we set com=time_window-1 so we get decay alpha=1/time_window
        up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
        down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

        rs = abs(up_chg_avg / down_chg_avg)
        rsi = 100 - 100 / (1 + rs)
        return rsi

#start_requests(ticker)

if __name__ == "__main__":
        ticker = 'NICA'

        #start_requests(ticker)

        app = QtWidgets.QApplication(sys.argv)
        mainwindow = QtWidgets.QMainWindow()
        ui = ui_mainwindow()
        ui.setupui(mainwindow)
        mainwindow.show()
        sys.exit(app.exec_())



