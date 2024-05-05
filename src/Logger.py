import logging, os
def Set_Ut_Logger(location, level, fileName):
    if location == "":
        location = os.path.dirname(fileName) + "/log/" + os.path.basename(fileName).split(".")[0] + ".log"

    if level == "":
        level = 'DEBUG'

    log_level_dict = {'NOTSET': logging.NOTSET, 'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                      'WARN': logging.WARN, 'ERROR': logging.ERROR, 'FATAL': logging.FATAL}
    print(f"Wrtie log at:{location}")

    # 로거 생성 및 로그 레벨 설정
    logger = logging.getLogger(os.path.basename(fileName).split(".")[0])
    logger.setLevel(log_level_dict[level])  # 모든 레벨의 로그를 캡처하도록 설정

    # 파일 핸들러 생성 및 로그 레벨 설정
    file_handler = logging.FileHandler(location)
    file_handler.setLevel(log_level_dict[level])  # ERROR 및 그 이상의 로그만 파일로 기록

    # # 콘솔 핸들러 생성 및 로그 레벨 설정
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(log_level_dict[level])  # INFO 및 그 이상의 로그만 콘솔에 출력

    # 로그 메시지 형식 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # console_handler.setFormatter(formatter)

    # 핸들러를 로거에 추가
    logger.addHandler(file_handler)
    # logger.addHandler(console_handler)

    # 로그 메시지 테스트
    # logger.debug('This is a debug message')
    # logger.info('This is an info message')
    # logger.warning('This is a warning message')
    # logger.error('This is an error message')
    # logger.critical('This is a critical message')

    return logger

