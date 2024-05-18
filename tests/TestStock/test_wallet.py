import os, unittest, logging                    # Don't touch
from src.Logger import Set_Ut_Logger            # Don't touch


import yfinance as yf
import pandas as pd
from src.Stock.Wallet import Wallet

class TestWallet(unittest.TestCase):
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

    def test_wallet1(self):
        """Test case 1: Calulate RSI using APPL's 1wk candles"""
        df = yf.download(tickers="AAPL", start="2023-01-01", end="2024-05-06", interval="1wk")
        wl = Wallet(logger=self.logger)
        wl.buy("APPL",df.iloc[-1]["Close"], df.index[-1])
        wl.sell("APPL", df.iloc[-1]["Close"], df.index[-1])

    def test_wallet_getHistory(self):
        """Test case 1: Calulate RSI using APPL's 1wk candles"""
        df = yf.download(tickers="AAPL", start="2023-01-01", end="2024-05-06", interval="1wk")
        wl = Wallet(logger=self.logger)
        wl.buy("APPL", df.iloc[-2]["Close"], df.index[-2])
        wl.sell("APPL", df.iloc[-1]["Close"], df.index[-1])
        df['BUY'], df['SELL'] = wl.get_history()
        self.logger.info(f"{df.tail(5)}")



if __name__ == '__main__':
    unittest.main()