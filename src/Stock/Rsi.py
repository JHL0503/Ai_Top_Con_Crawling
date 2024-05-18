import pandas as pd
import numpy as np

from src.Stock.MA import RMA
def Rsi(source, period=14):
    # 가격 차이를 계산
    delta = source.diff()

    # 이익과 손실을 분리
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    # 평균 이익과 평균 손실을 지수 이동 평균으로 계산
    average_gain = RMA(gain, period)
    average_loss = RMA(loss, period)


    # RS (Relative Strength) 계산
    tmp = []
    for idx in average_gain.index:
        if(average_gain[idx] != np.nan and average_loss[idx] != np.nan):
            tmp.append(average_gain[idx]/average_loss[idx])
        else:
            tmp.append(np.nan)
    rs = pd.Series(tmp)
    rs.index = average_gain.index

    # RSI 계산
    rsi = rs.apply(lambda x: (100 - (100 / (1 + x))) if ~np.isnan(x) else np.nan)

    return rsi
