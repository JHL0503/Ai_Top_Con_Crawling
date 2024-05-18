import os, unittest, logging                    # Don't touch
from src.Logger import Set_Ut_Logger            # Don't touch


import yfinance as yf
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

from src.Stock.Rsi import Rsi
from src.Stock.Stochastic import Stochastic
from src.Stock.MA import SMA, RMA
from src.Stock.MyIndi import StochasticRSI

class TestStock(unittest.TestCase):
    LOG_LOCATION = os.getenv('LOG_LOCATION', "")                # Don't touch
    LOG_LEVEL = os.getenv('LOG_LEVEL', "")                      # Don't touch
    logger = Set_Ut_Logger(LOG_LOCATION, LOG_LEVEL, __file__)   # Don't touch

    @classmethod
    def setUpClass(cls):
        # 전체 테스트 전 초기화 과정
        cls.logger.info("hi")

    @classmethod
    def tearDownClass(cls):
        # 전체 테스트 후 초기화 과정
        cls.logger.info("bye")

    def setUp(self):
        # 매 개별 테스트 전 초기화 과정
        self.logger.info("=========================")
        self.logger.info("Setup for test: %s", self.shortDescription())

    def tearDown(self):
        # 매 개별 테스트 후 정리 과정
        self.logger.info("Teardown for test: %s", self.shortDescription())

    def test_sma(self):
        """Test case 1: Calulate RSI using APPL's 1wk candles"""
        df = yf.download(tickers="AAPL", start="2023-01-01", end="2024-05-06", interval="1wk")
        df['sma5'] = SMA(source=df['Close'], length=5)
        df['sma20'] = SMA(source=df['Close'], length=20)
        df['sma60'] = SMA(source=df['Close'], length=60)
        df['sma120'] = SMA(source=df['Close'], length=120)
        self.logger.info(df.iloc[-2])

    def test_rma(self):
        """Test case 1: Calulate RSI using APPL's 1wk candles"""
        df = yf.download(tickers="AAPL", start="2023-01-01", end="2024-05-06", interval="1wk")
        df['rma14'] = RMA(source=df['Close'], length=14)
        self.logger.info(df.iloc[-2])

    def test_stoch(self):
        """Test case 1: Calulate RSI using APPL's 1wk candles"""
        df = yf.download(tickers="AAPL", start="2023-01-01", end="2024-05-06", interval="1wk")
        stoch = Stochastic(source=df['Close'], high=df['High'], low=df['Low'], length=14)
        df['stoch_K'] = SMA(source=stoch, length=1)
        df['stoch_D'] = SMA(source=df['stoch_K'], length=3)
        self.logger.info(df.iloc[-2])
    def test_rsi(self):
        """Test case 1: Calulate RSI using APPL's 1wk candles"""
        df = yf.download(tickers="AAPL", start="2023-01-01", end="2024-05-06", interval="1wk")
        df['RSI'] = Rsi(source=df['Close'], period=14)
        self.logger.info(df.iloc[-2])

    def test_stochastic_rsi(self):
        """Test case 2: Stochastic RSI"""
        df = yf.download(tickers="AAPL", start="2023-01-01", end="2024-05-06", interval="1wk")
        df['StochasticRSI'] = StochasticRSI(df['Close'])
        self.logger.info(df.tail())
        self.logger.info(df.iloc[-1])
        self.logger.info(df.iloc[-2])
        self.logger.info(df.iloc[-3])


if __name__ == '__main__':
    unittest.main()