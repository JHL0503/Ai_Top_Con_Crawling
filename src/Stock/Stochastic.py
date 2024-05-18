import pandas as pd
import numpy as np


def Stochastic(source, high, low, length=14):
    # 최근 k_period 일 동안의 최고가와 최저가를 계산
    low_min = low.rolling(window=length).min()
    high_max = high.rolling(window=length).max()

    stochastic = ((source - low_min) / (high_max - low_min)) * 100

    return stochastic
