import os, unittest, logging                    # Don't touch
from src.Logger import Set_Ut_Logger            # Don't touch

class TestTemplate(unittest.TestCase):
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

    def test_case1(self):
        """Test case 1: Example description for this test case."""
        result = 3  # 적절한 인수를 사용하세요.
        self.assertEqual(result, 3)
        self.logger.info("test_case1 passed.")

    def test_case2(self):
        """Test case 2: Another description for this test case."""
        result = 7  # 적절한 인수를 사용하세요.
        self.assertEqual(result, 7)
        self.logger.info("test_case2 passed.")

if __name__ == '__main__':
    unittest.main()