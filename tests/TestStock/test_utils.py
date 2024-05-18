import os, unittest, logging                    # Don't touch
from src.Logger import Set_Ut_Logger            # Don't touch


import yfinance as yf
import pandas as pd
from src.Stock.Wallet import Wallet
from src.Stock.Utils import check_ticker_validity, get_exact_ticker_name
class TestUtils(unittest.TestCase):
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

    def test_check_ticker_validity(self):
        self.assertEqual(check_ticker_validity("005930.KS"), True)
        self.assertEqual(check_ticker_validity("036220.KQ"), True)
        self.assertEqual(check_ticker_validity("005122.KQ"), False)

    def test_get_exact_ticker_name(self):
        self.assertEqual(get_exact_ticker_name("5930"), "005930.KS")
        self.assertEqual(get_exact_ticker_name("036220"), "036220.KQ")
        self.assertEqual(get_exact_ticker_name("005122"), None)


if __name__ == '__main__':
    unittest.main()