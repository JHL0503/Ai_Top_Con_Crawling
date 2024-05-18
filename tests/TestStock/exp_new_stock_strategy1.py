####################################################################################
# 신규주 투자 전략
# 기본가설:
#   첫날 양봉으로 마무리 된 신규주는 다음날 갭상승으로 시작한다. 그 갭차를 먹고 바로 파는 전략.
# 내용:
#   상장일, 다음날 주가만을 가지고 한번 실험해보자.
#   방식 1: 무조건 사고 판다. 바로 상간건 못샀다고 하고.
####################################################################################
import os, unittest, logging                    # Don't touch
from src.Logger import Set_Ut_Logger,get_local_dir_path            # Don't touch

import yfinance as yf
import pandas as pd
from tqdm import tqdm
from src.Stock.QuantEvaluator import QuantEvaluator
import matplotlib.pyplot as plt

LOCAL_LOG_PATH, LOCAL_DATA_PATH = get_local_dir_path(__file__)
LOG_LOCATION = os.getenv('LOG_LOCATION', "")  # Don't touch
LOG_LEVEL = os.getenv('LOG_LEVEL', "")  # Don't touch
logger = Set_Ut_Logger(LOG_LOCATION, LOG_LEVEL, __file__, 'w')  # Don't touch


def strategy1(strategy_name, df):
    SEED_MONEY = 1000
    Money = SEED_MONEY
    qe = QuantEvaluator(strategy_name)

    tmp_columns = ['샀는지', '수익률(%)', '총자본']
    tmp_df = pd.DataFrame(index=df.index, columns=tmp_columns)
    for i in tqdm(range(len(df) - 1, -1, -1)):
        item = df.iloc[i]
        Close_1 = item['Close_1']
        High_1 = item['High_1']
        Open_2 = item['Open_2']
        Date = item['상장일']
        Change = (Open_2 - Close_1) / Close_1
        Change_P = ("%.2f" % (Change * 100))

        if High_1 == Close_1:  # 아마 시작하자 마자 상 간거라서 못샀을거 같다.
            tmp_list = ['-', Change_P, Money]
        else:
            Money += Money * (Change)
            qe.put_transaction(Date, Money)
            tmp_list = ['BUY', Change_P, Money]

        tmp_df.iloc[i] = tmp_list

    # 4. 결과 정리하기
    new_df = pd.concat([df, tmp_df], axis=1)
    res1, res2 = qe.evaluate()


    # 5. 결과 저장하기
    fig, axes = plt.subplots(2, 1)
    res1.plot(x='date', y='balance', kind='line', ax=axes[0])
    res1.plot(x='date', y='MDD', kind='line', ax=axes[1])
    # plt.show()
    plt.savefig(f'{strategy_name}.png')
    new_df.to_excel(strategy_name +'.xlsx', index=False)

    return res2

def strategy3(strategy_name, df):
    SEED_MONEY = 1000
    Money = SEED_MONEY
    qe = QuantEvaluator(strategy_name)

    tmp_columns = ['샀는지', '수익률(%)', '총자본']
    tmp_df = pd.DataFrame(index=df.index, columns=tmp_columns)
    for i in tqdm(range(len(df) - 1, -1, -1)):
        item = df.iloc[i]
        Open_1 = item['Open_1']
        Close_1 = item['Close_1']
        High_1 = item['High_1']
        Open_2 = item['Open_2']
        Date = item['상장일']
        Change = (Open_2 - Close_1) / Close_1
        Change_P = ("%.2f" % (Change * 100))
        stock_cmp = item['상장주선인']

        if High_1 == Close_1:  # 아마 시작하자 마자 상 간거라서 못샀을거 같다.
            tmp_list = ['-', Change_P, Money]
        elif '미래' in stock_cmp:  # 미래에셋꺼는 재낀다.
            tmp_list = ['-', Change_P, Money]
        elif Close_1 < Open_1:  # 양봉 마무리만 산다.
            tmp_list = ['-', Change_P, Money]
        else:
            Money += Money * (Change)
            qe.put_transaction(Date, Money)
            tmp_list = ['BUY', Change_P, Money]

        tmp_df.iloc[i] = tmp_list

    # 4. 결과 정리하기
    new_df = pd.concat([df, tmp_df], axis=1)
    res1, res2 = qe.evaluate()

    # 5. 결과 저장하기
    fig, axes = plt.subplots(2, 1)
    res1.plot(x='date', y='balance', kind='line', ax=axes[0])
    res1.plot(x='date', y='MDD', kind='line', ax=axes[1])
    # plt.show()
    plt.savefig(f'{strategy_name}.png')
    new_df.to_excel(strategy_name + '.xlsx', index=False)

    return res2

def strategy4(strategy_name, df, percent):
    """
    시초가에 무조건 사서 가만히 둬보기
    """
    SEED_MONEY = 1000
    Money = SEED_MONEY
    qe = QuantEvaluator(strategy_name)

    tmp_columns = ['샀는지', '수익률(%)', '총자본']
    tmp_df = pd.DataFrame(index=df.index, columns=tmp_columns)
    for i in tqdm(range(len(df) - 1, -1, -1)):
        item = df.iloc[i]
        Open_1 = item['Open_1']
        Close_1 = item['Close_1']

        Date = item['상장일']
        Change = (Close_1 - Open_1) / Open_1
        Change_P = ("%.2f" % (Change * 100))
        stock_cmp = item['상장주선인']

        if '미래' in stock_cmp:  # 미래에셋꺼는 재낀다.
            tmp_list = ['-', Change_P, Money]
        else:
            Money += (Money * percent) * (Change)
            qe.put_transaction(Date, Money)
            tmp_list = ['BUY', Change_P, Money]

        tmp_df.iloc[i] = tmp_list

    # 4. 결과 정리하기
    new_df = pd.concat([df, tmp_df], axis=1)
    res1, res2 = qe.evaluate()

    # 5. 결과 저장하기
    fig, axes = plt.subplots(2, 1)
    res1.plot(x='date', y='balance', kind='line', ax=axes[0])
    res1.plot(x='date', y='MDD', kind='line', ax=axes[1])
    # plt.show()
    plt.savefig(f'{strategy_name}.png')
    new_df.to_excel(strategy_name + '.xlsx', index=False)

    return res2


def strategy5(strategy_name, df, percent):
    SEED_MONEY = 1000
    Money = SEED_MONEY
    qe = QuantEvaluator(strategy_name)

    tmp_columns = ['샀는지', '수익률(%)', '총자본']
    tmp_df = pd.DataFrame(index=df.index, columns=tmp_columns)
    for i in tqdm(range(len(df) - 1, -1, -1)):
        item = df.iloc[i]
        Close_1 = item['Close_1']
        High_1 = item['High_1']
        Open_2 = item['Open_2']
        Date = item['상장일']
        Change = (Open_2 - Close_1) / Close_1
        Change_P = ("%.2f" % (Change * 100))
        stock_cmp = item['상장주선인']

        if High_1 == Close_1:  # 아마 시작하자 마자 상 간거라서 못샀을거 같다.
            tmp_list = ['-', Change_P, Money]
        elif '미래' in stock_cmp:  # 미래에셋꺼는 재낀다.
            tmp_list = ['-', Change_P, Money]
        else:
            Money += Money * percent * (Change)
            qe.put_transaction(Date, Money)
            tmp_list = ['BUY', Change_P, Money]

        tmp_df.iloc[i] = tmp_list

    # 4. 결과 정리하기
    new_df = pd.concat([df, tmp_df], axis=1)
    res1, res2 = qe.evaluate()

    # 5. 결과 저장하기
    fig, axes = plt.subplots(2, 1)
    res1.plot(x='date', y='balance', kind='line', ax=axes[0])
    res1.plot(x='date', y='MDD', kind='line', ax=axes[1])
    # plt.show()
    plt.savefig(f'{strategy_name}.png')
    new_df.to_excel(strategy_name + '.xlsx', index=False)

    return res2


def strategy6(strategy_name, df, percent):
    SEED_MONEY = 1000
    Money = SEED_MONEY
    qe = QuantEvaluator(strategy_name)

    tmp_columns = ['샀는지', '수익률(%)', '총자본']
    tmp_df = pd.DataFrame(index=df.index, columns=tmp_columns)
    for i in tqdm(range(len(df) - 1, -1, -1)):
        item = df.iloc[i]
        Open_1 = item['Open_1']
        Close_1 = item['Close_1']
        High_1 = item['High_1']
        Open_2 = item['Open_2']
        Date = item['상장일']
        Change = (Open_2 - Close_1) / Close_1
        Change_P = ("%.2f" % (Change * 100))
        stock_cmp = item['상장주선인']

        if High_1 == Close_1:  # 아마 시작하자 마자 상 간거라서 못샀을거 같다.
            tmp_list = ['-', Change_P, Money]
        elif '미래' in stock_cmp:  # 미래에셋꺼는 재낀다.
            tmp_list = ['-', Change_P, Money]
        elif Close_1 < Open_1:  # 음봉에는 percent
            Money += Money * percent * (Change)
            qe.put_transaction(Date, Money)
            tmp_list = ['BUY', Change_P, Money]
        else: # 양봉에는 full
            Money += Money * (Change)
            qe.put_transaction(Date, Money)
            tmp_list = ['BUY', Change_P, Money]

        tmp_df.iloc[i] = tmp_list

    # 4. 결과 정리하기
    new_df = pd.concat([df, tmp_df], axis=1)
    res1, res2 = qe.evaluate()

    # 5. 결과 저장하기
    fig, axes = plt.subplots(2, 1)
    res1.plot(x='date', y='balance', kind='line', ax=axes[0])
    res1.plot(x='date', y='MDD', kind='line', ax=axes[1])
    # plt.show()
    plt.savefig(f'{strategy_name}.png')
    new_df.to_excel(strategy_name + '.xlsx', index=False)

    return res2

def strategy7(strategy_name, df, ratio):
    SEED_MONEY = 1000
    Money = SEED_MONEY
    qe = QuantEvaluator(strategy_name)

    tmp_columns = ['샀는지', '수익률(%)', '총자본']
    tmp_df = pd.DataFrame(index=df.index, columns=tmp_columns)
    for i in tqdm(range(len(df) - 1, -1, -1)):
        item = df.iloc[i]
        Open_1 = item['Open_1']
        Close_1 = item['Close_1']
        High_1 = item['High_1']
        Open_2 = item['Open_2']
        Date = item['상장일']
        Change = (Open_2 - Close_1) / Close_1
        Change_P = ("%.2f" % (Change * 100))
        stock_cmp = item['상장주선인']

        if High_1 == Close_1:  # 아마 시작하자 마자 상 간거라서 못샀을거 같다.
            tmp_list = ['-', Change_P, Money]
        elif '미래' in stock_cmp:  # 미래에셋꺼는 재낀다.
            tmp_list = ['-', Change_P, Money]
        elif Close_1 < Open_1:  # 음봉에는 재낀다.
            tmp_list = ['-', Change_P, Money]
        else: # 양봉 중에서도
            if ((Open_1+High_1) / (1/ratio)) <= Close_1:
                Money += Money * (Change)
                qe.put_transaction(Date, Money)
                tmp_list = ['BUY', Change_P, Money]
            else:
                tmp_list = ['-', Change_P, Money]

        tmp_df.iloc[i] = tmp_list

    # 4. 결과 정리하기
    new_df = pd.concat([df, tmp_df], axis=1)
    res1, res2 = qe.evaluate()

    # 5. 결과 저장하기
    fig, axes = plt.subplots(2, 1)
    res1.plot(x='date', y='balance', kind='line', ax=axes[0])
    res1.plot(x='date', y='MDD', kind='line', ax=axes[1])
    # plt.show()
    plt.savefig(f'{strategy_name}.png')
    new_df.to_excel(strategy_name + '.xlsx', index=False)

    return res2

if __name__ == "__main__":
    print(f"Used data file name: {LOCAL_DATA_PATH + '/IPO_Total_add_delisting.xlsx'}")
    df = pd.read_excel(LOCAL_DATA_PATH + '/IPO_Total_add_delisting.xlsx')

    score_list = []
    strategy_name = 'ipo_stg_항상산다'
    score_list.append(strategy1(strategy_name, df))

    strategy_name = 'ipo_stg_항상산다_미래빼고_자본의30%로'
    score_list.append(strategy5(strategy_name, df, 0.3))
    strategy_name = 'ipo_stg_항상산다_미래빼고_자본의40%로'
    score_list.append(strategy5(strategy_name, df, 0.4))
    strategy_name = 'ipo_stg_항상산다_미래빼고_자본의50%로'
    score_list.append(strategy5(strategy_name, df, 0.5))
    strategy_name = 'ipo_stg_항상산다_미래빼고_자본의100%로'
    score_list.append(strategy5(strategy_name, df, 1.0))

    strategy_name = 'ipo_stg_양봉에만산다_미래빼고'
    score_list.append(strategy3(strategy_name, df))

    strategy_name = 'ipo_stg_양봉에는100_음봉에는20_미래빼고'
    score_list.append(strategy6(strategy_name, df, 0.2))
    strategy_name = 'ipo_stg_양봉에는100_음봉에는30_미래빼고'
    score_list.append(strategy6(strategy_name, df, 0.3))
    strategy_name = 'ipo_stg_양봉에는100_음봉에는40_미래빼고'
    score_list.append(strategy6(strategy_name, df, 0.4))

    strategy_name = 'ipo_stg_양봉중10%이상에100_미래빼고'
    score_list.append(strategy7(strategy_name, df, 0.1))
    strategy_name = 'ipo_stg_양봉중20%이상에100_미래빼고'
    score_list.append(strategy7(strategy_name, df, 0.2))
    strategy_name = 'ipo_stg_양봉중30%이상에100_미래빼고'
    score_list.append(strategy7(strategy_name, df, 0.3))
    strategy_name = 'ipo_stg_양봉중40%이상에100_미래빼고'
    score_list.append(strategy7(strategy_name, df, 0.4))

    ## + 여기에 만약 +로 시초가로 시작하면 몇퍼 더 먹어진다. 그리고 - 시초가로 시작하면 무조건
    ## 바로 파는게 맞다.
    strategy_name = 'ipo_stg_양봉중50%이상에100_미래빼고'
    score_list.append(strategy7(strategy_name, df, 0.5))


    strategy_name = 'ipo_stg_시초가에무조건산다_자본의1%로'
    score_list.append(strategy4(strategy_name, df, 0.01))


    score_df = pd.DataFrame(score_list)
    score_df.to_csv('score.csv', sep='\t', index=False)
