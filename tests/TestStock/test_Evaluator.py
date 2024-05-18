import os, unittest, logging                    # Don't touch
from src.Logger import Set_Ut_Logger            # Don't touch


import yfinance as yf
import pandas as pd

from src.Stock.QuantEvaluator import QuantEvaluator

class TestEvaluator(unittest.TestCase):
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

    def test_get_history(self):
        qe = QuantEvaluator(strategy_name="Test", logger=self.logger)
        qe.put_transaction(date="2024-05-02  12:00:00", balance=1000)
        qe.put_transaction(date="2024-05-03  12:00:00", balance=1100)
        qe.put_transaction(date="2024-05-04  12:00:00", balance=1000)
        qe.put_transaction(date="2024-05-05  12:00:00", balance=1300)
        df, statics = qe.evaluate()




if __name__ == '__main__':
    unittest.main()