import os, unittest, logging                    # Don't touch
from src.Logger import Set_Ut_Logger            # Don't touch


import yfinance as yf
import mplfinance as mpf
import pandas as pd
import numpy as np

from src.Stock.MyIndi import StochasticRSI
from src.Stock.Wallet import Wallet

LOG_LOCATION = os.getenv('LOG_LOCATION', "")  # Don't touch
LOG_LEVEL = os.getenv('LOG_LEVEL', "")  # Don't touch
logger = Set_Ut_Logger(LOG_LOCATION, LOG_LEVEL, __file__, 'w')  # Don't touch


# 1. 주식 값 받는다.
# "MSFT", "NVDA", "AAPL", "AMZN", "TSLA", "QCOM", "ASML", "META", "GOOG", "TSM", "TQQQ",
# "AMD", "INTC", "XOM", "V", "MU" , "TQQQ, SOXL, BULZ, FNGU"
stock_code = "SOXL"
# df = yf.download(tickers="AAPL", start="2023-01-01", end="2024-05-06", interval="1wk")
df = yf.download(tickers=stock_code, start="2022-01-01", end="2024-05-06", interval="1wk")
# df = yf.download(tickers=stock_code, start="2015-01-01", end="2024-05-06", interval="1d")
# df = yf.download(tickers=stock_code, interval="1wk")

# 2. Indicator 생성한다.
df['stochasticRSI_k'], df['stochasticRSI_d']= StochasticRSI(source=df['Close'])

# 3. 진행하면서 사고 팔자
state = 0
wl = Wallet(logger=logger)
prev_rsi = 0
UPPER_LIMIT = 85
UPPER_SELL = 80
LOWER_BUY = 15
LOWER_LIMT = 10
BUY_PERSENT = 0.25
for i in range(len(df)):
    # 이번주 지표
    time = df.index[i]
    price = df.iloc[i]['Close']
    stochRsi = df.iloc[i]['stochasticRSI_k']

    # state 0 에서 20이하 찍으면 1로 바뀌고
    if(state==0 and stochRsi<LOWER_LIMT):
        state = 1
    # 그러다 state 1 에서 20 넘으면 사고나서 state 2로 바뀐다.
    elif (state == 1 and stochRsi > LOWER_BUY):
        wl.buy(stock_code, price, time, percent=BUY_PERSENT)
        state = 2
    # (추가됨) 80으로 가는 줄 알았는데 다시 꼬꾸라지면
    elif (state == 2 and stochRsi < LOWER_LIMT):
        state = 1
    # 그러나 state 2에서 80 넘으면 팔 준비하기 위해서 3으로 바뀌고
    elif (state == 2 and stochRsi > UPPER_LIMIT):
        prev_rsi = stochRsi
        state = 3

    # 그러나 state 3에서는 이제 아래의 조건으로 '판매'가 tirgger 된다
    # 1. RSI가 80 이하로 떨어지던가.
    # 2. 이전 RSI 보다 낮아졌는데 그게 5이상 차이면. 넘으면 팔 준비하기 위해서 3으로 바뀌고
    elif (state == 3):
        if(stochRsi < UPPER_SELL):
            wl.sell(stock_code, price, time)
            state = 0
        elif(prev_rsi > stochRsi and (prev_rsi-stochRsi) >= 5):
            wl.sell(stock_code, price, time)
            state = 0

        prev_rsi = stochRsi

# 4. 사고 판 history 받고
df['BUY'], df['SELL'] = wl.get_history()
Buy_mks = []
Sell_mks = []
for i in range(len(df)):
    if pd.isna(df.iloc[i]['BUY']):
        Buy_mks.append("")
    else:
        Buy_mks.append("$B$")

    if pd.isna(df.iloc[i]['SELL']):
        Sell_mks.append("")
    else:
        Sell_mks.append("$S$")



# 5. Graph 그린다.
plots = [
    mpf.make_addplot(df['Close'],type='scatter',marker=Buy_mks, color='b', markersize=45,panel=0),
    mpf.make_addplot(df['Close'],type='scatter',marker=Sell_mks,color='r',markersize=45,panel=0),

    mpf.make_addplot(df['stochasticRSI_k'], panel=2),
    mpf.make_addplot(df['stochasticRSI_d'], panel=2),
    mpf.make_addplot(df['stochasticRSI_k'], type='scatter', marker=Buy_mks, color='b', markersize=45, panel=2),
    mpf.make_addplot(df['stochasticRSI_k'], type='scatter', marker=Sell_mks, color='r', markersize=45, panel=2),
]

# mpf.plot(df, type='candle', style='charles', volume=True, title='Sample Candlestick Chart',mav=(5, 20), ylabel='Price ($)',
#          addplot=plots, savefig="HI.png")
mpf.plot(df, type='candle', style='charles', volume=True, title='Sample Candlestick Chart',mav=(5, 20, 40), ylabel='Price ($)',
         addplot=plots)

