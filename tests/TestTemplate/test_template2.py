import os, unittest, logging                                    # Don't touch

#
#
#
#
# print(my_var)
#
# class TestTemplate(unittest.TestCase):
#
#     def test_example(self):
#         a = 1
#         b = 2
#         print("HIHI")
#         self.assertEqual(a+b, 3)
#
#
# # 이 파일이 메인으로 실행될 때 유닛 테스트 실행
# if __name__ == '__main__':
#     unittest.main()
#
#
#
# from some_module import some_function  # 테스트할 함수를 임포트하세요.
#
# # 로깅 설정


class TestSomeFunction2(unittest.TestCase):
    LOG_LOCATION = os.getenv('LOG_LOCATION', os.path.dirname(__file__) + "/log/" + os.path.basename(
        __file__) + ".log")  # Don't touch
    LOG_LEVEL_DICT = {'NOTSET': logging.NOTSET, 'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                      'WARN': logging.WARN, 'ERROR': logging.ERROR, 'FATAL': logging.FATAL}  # Don't touch
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')  # Don't touch

    logger = logging.getLogger(os.path.basename(__name__))
    file_handler = logging.FileHandler(LOG_LOCATION, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)


    # @classmethod
    # def setUpClass(cls):

    #
    #     # cls.logger = logging.getLogger('TestClassOne')
    #     cls.logger = logging.getLogger(os.path.basename(__name__))
    #     print(__name__)
    #     # file_handler = logging.FileHandler(LOG_LOCATION, mode='w')
    #     cls.file_handler = logging.FileHandler(f'{__name__}.log', mode='a')
    #
    #     # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #     cls.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    #     cls.file_handler.setFormatter(cls.formatter)
    #     cls.logger.addHandler(cls.file_handler)
    #
    #
    # @classmethod
    # def tearDownClass(cls):
    #     handlers = cls.logger.handlers[:]
    #     for handler in handlers:
    #         handler.close()
    #         cls.logger.removeHandler(handler)


    # def setUp(self):
    #
    #     # 테스트 전 초기화 과정, 필요하다면 여기에서 설정
    #     self.logger.debug("Running TestClassOne test_case_one")
    #
    # def tearDown(self):
    #     # 테스트 후 정리 과정, 필요하다면 여기에서 설정
    #     self.logger.debug("Running TestClassOne test_case_one")

    def test_case1(self):
        print("H1")
        """Test case 1: Example description for this test case."""
        self.logger.info("Running TestClassOne test_case_one")

    def test_case2(self):
        print("H2")
        """Test case 2: Another description for this test case."""
        self.logger.info("Running TestClassOne test_case_one")
if __name__ == '__main__':
    unittest.main()