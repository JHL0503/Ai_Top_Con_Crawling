import pandas as pd
import numpy as np


def SMA(source, length=14):
    sma = source.rolling(window=length).mean()
    return sma

def RMA(source, length=14):
    alpha = 1/length
    sma = source.rolling(window=length).mean()

    rma = pd.Series(index=source.index)

    for i in range(len(source)):
        if i == 0:
            rma.iloc[i] = np.nan
        elif np.isnan(rma.iloc[i-1]):
            rma.iloc[i] = sma.iloc[i]
        else:
            rma.iloc[i] = (alpha * source.iloc[i]) + (1-alpha) * rma.iloc[i-1]

    # ema = source.ewm(span=length, adjust=False).mean()

    return rma
