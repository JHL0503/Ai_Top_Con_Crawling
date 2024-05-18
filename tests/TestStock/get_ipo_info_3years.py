####################################################################################
# 신규주 투자 전략
# 기본가설:
#   첫날 양봉으로 마무리 된 신규주는 다음날 갭상승으로 시작한다. 그 갭차를 먹고 바로 파는 전략.
# 내용:
#   확인을 위해서 기업공시채널 KIND에서 '신규상장기업현황' 에서 Excel로 신규상장 주식 리스트를 받았다.
#   다만 상장폐지 되는 등으로 야후 파이낸스에서 값을 못 읽어 오는 것들이 있다. 그걸 먼저 걸러낸다.
####################################################################################

import os, unittest, logging                    # Don't touch

import numpy as np

from src.Logger import Set_Ut_Logger,get_local_dir_path            # Don't touch

from src.Stock.Utils import get_exact_ticker_name

import pandas as pd
from tqdm import tqdm
import yfinance as yf

LOCAL_LOG_PATH, LOCAL_DATA_PATH = get_local_dir_path(__file__)
LOG_LOCATION = os.getenv('LOG_LOCATION', "")  # Don't touch
LOG_LEVEL = os.getenv('LOG_LEVEL', "")  # Don't touch
logger = Set_Ut_Logger(LOG_LOCATION, LOG_LEVEL, __file__, 'a')  # Don't touch


def step1():
    # 1. 엑셀 읽어 오기.
    file_path = LOCAL_DATA_PATH + '/KOSPI_IPO_3years.xlsx'
    df = pd.read_excel(file_path)

    # 3. 불필요한 것 지우기
    df = df[~df['회사명'].str.contains('스팩')]
    df = df[~df['회사명'].str.contains('투자')]
    df = df[df['증권구분'] == '주권']
    df = df.reset_index(drop=True)

    # 4. 추가 되어야 할 colum 빈 공간 미리 만들어 두기
    tmp_columns = ['State', 'Open_1', 'High_1', 'Low_1', 'Close_1', 'Volume_1', 'Open_2', 'High_2', 'Low_2', 'Close_2',
                   'Volume_2']
    tmp_df = pd.DataFrame(index=df.index, columns=tmp_columns)
    df = pd.concat([df, tmp_df], axis=1)

    df.to_excel(LOCAL_DATA_PATH + '/KOSPI_IPO_3years_1.xlsx', index=False)
    df.to_excel(LOCAL_DATA_PATH + '/KOSPI_IPO_3years_2.xlsx', index=False)

def step2():
    # 1. 엑셀 읽어 오기.
    file_path = LOCAL_DATA_PATH + '/KOSPI_IPO_3years_2.xlsx'
    df = pd.read_excel(file_path)

    # 2. '종목코드' 찾아 넣기.
    for i in tqdm(range(len(df))):
        if df.iloc[i]['State'] == 0 or np.isnan(df.iloc[i]['State']):
            try:
                Code = get_exact_ticker_name(df.iloc[i]['종목코드'])
                if Code == None:
                    logger.debug(f"delisting name:{df.iloc[i]['회사명']}, 상장일:{df.iloc[i]['상장일']}")
                    Code = "None"
                df.at[i, 'State'] = 1
                df.at[i, '종목코드'] = Code
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                df.at[i, 'State'] = 0

    df.to_excel(LOCAL_DATA_PATH + '/KOSPI_IPO_3years_2.xlsx', index=False)
    live_df = df[~(df['종목코드'] == 'None')]
    live_df.to_excel(LOCAL_DATA_PATH + '/KOSPI_IPO_3years_3.xlsx', index=False)

    delisting_df = df[df['종목코드'] == 'None']
    delisting_df.to_excel(LOCAL_DATA_PATH + '/KOSPI_IPO_3years_4.xlsx', index=False)

def step3():
    # 1. 엑셀 읽어 오기.
    file_path = LOCAL_DATA_PATH + '/KOSDAC_IPO_3years.xlsx'
    df = pd.read_excel(file_path)

    # 3. 불필요한 것 지우기
    df = df[~df['회사명'].str.contains('스팩')]
    df = df[~df['회사명'].str.contains('투자')]
    df = df[df['증권구분'] == '주권']
    df = df.reset_index(drop=True)

    # 4. 추가 되어야 할 colum 빈 공간 미리 만들어 두기
    tmp_columns = ['State', 'Open_1', 'High_1', 'Low_1', 'Close_1', 'Volume_1', 'Open_2', 'High_2', 'Low_2', 'Close_2',
                   'Volume_2']
    tmp_df = pd.DataFrame(index=df.index, columns=tmp_columns)
    df = pd.concat([df, tmp_df], axis=1)

    df.to_excel(LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_1.xlsx', index=False)
    df.to_excel(LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_2.xlsx', index=False)

def step4():
    # 1. 엑셀 읽어 오기.
    file_path = LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_2.xlsx'
    df = pd.read_excel(file_path)

    # 2. '종목코드' 찾아 넣기.
    for i in tqdm(range(len(df))):
    # for i in tqdm(range(40,60,1)):
        if df.iloc[i]['State'] == 0 or np.isnan(df.iloc[i]['State']):
            try:
                Code = get_exact_ticker_name(df.iloc[i]['종목코드'])
                if Code == None:
                    logger.debug(f"delisting name:{df.iloc[i]['회사명']}, 상장일:{df.iloc[i]['상장일']}")
                    Code = "None"
                df.at[i , 'State'] = 1
                df.at[i, '종목코드'] = Code
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                df.at[i, 'State'] = 0

    df.to_excel(LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_2.xlsx', index=False)
    live_df = df[~(df['종목코드'] == 'None')]
    live_df.to_excel(LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_3.xlsx', index=False)

    delisting_df = df[df['종목코드'] == 'None']
    delisting_df.to_excel(LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_4.xlsx', index=False)


def step5():
    # 1. 엑셀 읽어 오기.
    file_path = LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_3.xlsx'
    df = pd.read_excel(file_path)

    # 2. '종목코드' 찾아 넣기.
    for i in tqdm(range(len(df))):
        item = df.iloc[i]
        ticker_code = item['종목코드']
        stat_time = item['상장일']
        end_time = stat_time + + pd.Timedelta(days=15)  # consider weekend

        if df.iloc[i]['State'] == 1:
            try:
                price = yf.download(tickers=ticker_code, start=stat_time, end=end_time, interval="1d")
                df.at[i, 'Open_1'] = price.iat[0, 0]
                df.at[i, 'High_1'] = price.iat[0, 1]
                df.at[i, 'Low_1'] = price.iat[0, 2]
                df.at[i, 'Close_1'] = price.iat[0, 3]
                df.at[i, 'Volume_1'] = price.iat[0, 5]
                df.at[i, 'Open_2'] = price.iat[1, 0]
                df.at[i, 'High_2'] = price.iat[1, 1]
                df.at[i, 'Low_2'] = price.iat[1, 2]
                df.at[i, 'Close_2'] = price.iat[1, 3]
                df.at[i, 'Volume_2'] = price.iat[1, 5]
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                df.at[i, 'State'] = 1

    df.to_excel(LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_3.xlsx', index=False)

    # 1. 엑셀 읽어 오기.
    file_path = LOCAL_DATA_PATH + '/KOSPI_IPO_3years_3.xlsx'
    df = pd.read_excel(file_path)

    # 2. '종목코드' 찾아 넣기.
    for i in tqdm(range(len(df))):
        item = df.iloc[i]
        ticker_code = item['종목코드']
        stat_time = item['상장일']
        end_time = stat_time + + pd.Timedelta(days=15)  # consider weekend

        if df.iloc[i]['State'] == 1:
            try:
                price = yf.download(tickers=ticker_code, start=stat_time, end=end_time, interval="1d")
                df.at[i, 'Open_1'] = price.iat[0, 0]
                df.at[i, 'High_1'] = price.iat[0, 1]
                df.at[i, 'Low_1'] = price.iat[0, 2]
                df.at[i, 'Close_1'] = price.iat[0, 3]
                df.at[i, 'Volume_1'] = price.iat[0, 5]
                df.at[i, 'Open_2'] = price.iat[1, 0]
                df.at[i, 'High_2'] = price.iat[1, 1]
                df.at[i, 'Low_2'] = price.iat[1, 2]
                df.at[i, 'Close_2'] = price.iat[1, 3]
                df.at[i, 'Volume_2'] = price.iat[1, 5]
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                df.at[i, 'State'] = 1

    df.to_excel(LOCAL_DATA_PATH + '/KOSPI_IPO_3years_3.xlsx', index=False)

def step6():
    KOSPI_df = pd.read_excel(LOCAL_DATA_PATH + '/KOSPI_IPO_3years_3.xlsx')
    KOSDAC_df = pd.read_excel(LOCAL_DATA_PATH + '/KOSDAC_IPO_3years_3.xlsx')

    kospi_idx = 0
    kosdac_idx = 0
    total_idx = 0
    kospi_len = len(KOSPI_df)
    kosdac_len = len(KOSDAC_df)
    tmp_columns = ['State', 'Open_1', 'High_1', 'Low_1', 'Close_1', 'Volume_1', 'Open_2', 'High_2', 'Low_2', 'Close_2',
                   'Volume_2']
    total_df = pd.DataFrame(index=range(kospi_len+kosdac_len), columns=KOSDAC_df.columns)
    # print(total_df)

    while 1:
        if kospi_idx==kospi_len and kosdac_idx==kosdac_len:
            break
        elif kospi_idx==kospi_len:
            total_df.iloc[total_idx] = KOSDAC_df.iloc[kosdac_idx]
            total_idx += 1
            kosdac_idx += 1

        elif kosdac_idx==kosdac_len:
            total_df.iloc[total_idx] = KOSPI_df.iloc[kospi_idx]
            total_idx += 1
            kospi_idx += 1

        else:
            if KOSPI_df.iloc[kospi_idx]['상장일'] > KOSDAC_df.iloc[kosdac_idx]['상장일']:
                total_df.iloc[total_idx] = KOSPI_df.iloc[kospi_idx]
                total_idx += 1
                kospi_idx += 1
            elif KOSPI_df.iloc[kospi_idx]['상장일'] < KOSDAC_df.iloc[kosdac_idx]['상장일']:
                total_df.iloc[total_idx] = KOSDAC_df.iloc[kosdac_idx]
                total_idx += 1
                kosdac_idx += 1
            else:
                total_df.iloc[total_idx] = KOSPI_df.iloc[kospi_idx]
                total_idx += 1
                kospi_idx += 1
                total_df.iloc[total_idx] = KOSDAC_df.iloc[kosdac_idx]
                total_idx += 1
                kosdac_idx += 1

    total_df.to_excel(LOCAL_DATA_PATH + '/IPO_Total.xlsx', index=False)

def step7():
    """
    3년 이내의 상장폐지된건 KIND 에 직접 들어가서 찾아서 채워 넣어야 한다!
    """
    print("Do yourself")

if __name__ == "__main__":
    print("HI")
    # step1()
    # step2()
    # step3()
    # step4()
    # step5()
    # step6()
    # step7()