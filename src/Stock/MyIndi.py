import pandas as pd
import numpy as np

from src.Stock.Rsi import Rsi
from src.Stock.Stochastic import Stochastic
from src.Stock.MA import SMA
def StochasticRSI(source, smookthK=3, smoothD=3, lengthRsi=14, lengthStoch=14):
    rsi = Rsi(source=source, period=lengthRsi)
    stock = Stochastic(source=rsi, high=rsi, low=rsi, length=lengthStoch)
    stochasticRSI_k = SMA(source=stock, length=smookthK)
    stochasticRSI_d = SMA(source=stochasticRSI_k, length=smoothD)

    return stochasticRSI_k, stochasticRSI_d