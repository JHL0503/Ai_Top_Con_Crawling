import yfinance as yf
import json


def read_jsonl(file_path):
    dict_list = []
    with open(file_path, 'r') as file:
        for line in file:
            dict_list.append(json.loads(line.strip()))
    return dict_list

def write_jsonl(dict_list, file_path):
    with open(file_path, 'w') as file:
        for item in dict_list:
            file.write(json.dumps(item) + '\n')

def check_ticker_validity(ticker_symbol):
    # 주어진 티커로 yfinance 객체 생성
    ticker = yf.Ticker(ticker_symbol)

    # 해당 티커의 정보 가져오기
    info = ticker.info

    # info 딕셔너리가 비어 있는지 확인
    if not info or 'regularMarketOpen' not in info or info['regularMarketOpen'] is None:
        return False
    else:
        return True



def get_exact_ticker_name(ticker_symbol: str):
    """
    엑셀 속에 있는 종목코드(tiker)는 한국 코드이다. 야후파이낸스에서는 해당 종목 코드에 +.KS, +.KQ 등을
    붙여야 한다. 그리고 상장 폐지 된 녀석들은 검색이 안된다. 이 함수의 역할을 아래와 같다.
    1. 042203과 같이 앞 자리가 0이 나오더라도 다 살려내야한다.
    2. .KS와 .KQ 중 무엇을 붙여야 하는지 알아낸다.
    3. 상장폐지 되었을 경우 None을 반환한다.
    """

    # 1. 앞자리 0 살리기.
    tmp_ticker = "%06d" % (int(ticker_symbol))

    # 2. .KS 인지 .KQ 인지 상장폐지인지 확인하기
    tmp_ticker1 = tmp_ticker + '.KS'
    if(check_ticker_validity(tmp_ticker1) == True):
        return tmp_ticker1

    tmp_ticker2 = tmp_ticker + '.KQ'
    if (check_ticker_validity(tmp_ticker2) == True):
        return tmp_ticker2

    return None