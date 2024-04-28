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


class TestSomeFunction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LOG_LOCATION = os.getenv('LOG_LOCATION', os.path.dirname(__file__) + "/log/" + os.path.basename(
            __file__) + ".log")  # Don't touch
        LOG_LEVEL_DICT = {'NOTSET': logging.NOTSET, 'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                          'WARN': logging.WARN, 'ERROR': logging.ERROR, 'FATAL': logging.FATAL}  # Don't touch
        LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')  # Don't touch

        cls.logger = logging.getLogger(os.path.basename(__file__))
        file_handler = logging.FileHandler(LOG_LOCATION)
        file_handler.setLevel(LOG_LEVEL_DICT[LOG_LEVEL])
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        cls.logger.addHandler(file_handler)
        print(id(cls.logger), "TestSomeFunction\n")

    @classmethod
    def tearDownClass(cls):
        # 테스트 전 초기화 과정, 필요하다면 여기에서 설정
        for handler in cls.logger.handlers[:]:  # 리스트 복사본을 만들어 반복
            handler.close()
            cls.logger.removeHandler(handler)
    def setUp(self):
        # 테스트 전 초기화 과정, 필요하다면 여기에서 설정

        self.logger.info("Setup for test: %s", self.shortDescription())

    def tearDown(self):
        # 테스트 후 정리 과정, 필요하다면 여기에서 설정
        self.logger.info("Teardown for test: %s", self.shortDescription())
        self.logger.info("---------------------------------------------------")

    def test_case1(self):
        """Test case 1: Example description for this test case."""
        result = 3  # 적절한 인수를 사용하세요.
        self.assertEqual(result, 3)
        self.logger.info("Test case 333 passed.")

    def test_case2(self):
        """Test case 2: Another description for this test case."""
        result = 7  # 적절한 인수를 사용하세요.
        self.assertEqual(result, 7)
        self.logger.info("Test case 444 passed.")

if __name__ == '__main__':
    unittest.main()