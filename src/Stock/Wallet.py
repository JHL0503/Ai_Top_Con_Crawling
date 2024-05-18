# 지갑의 기능을 적어보겠다.
# 기본 돈이있다.
# 사고 팔 수 있다.
# 분할 매수 분말 매도가 가능하게 사고 팔 때 %를 정할 수 있게 하자.
# 소수점은 버리게 만든다.
# history 저장해 놨다가 나중에 한번에 뱉어낸다.

import logging
import math
import pandas as pd

class Wallet:

    def __init__(self, balance=10000, tax=0.0007, logger=None):
        self.init_balance = balance
        self.curr_expect_balance = balance
        self.curr_balance = balance
        self.tax = tax
        self.stocks = dict()
        self.profit = 0
        self.history = pd.DataFrame(columns=['BUY', 'SELL'])
        self.logger = logger


    def buy(self, stock_code, price, time, percent=0.125):
        # 이번에 사는데 쓸 수 있는 총 돈 (소수점은 내림한다)
        try_budget = math.floor(self.curr_expect_balance * percent)

        # budget을 진짜 내가 가진 돈(curr_balance) 에서 구하는게 아니기에
        # 확인 해야한다.
        real_budget = try_budget if (try_budget <= self.curr_balance) else self.curr_balance

        # price에 세금 더해서 먼저 총 살 수 있는 stock 갯수 구하자 (소수점은 내림한다)
        num_buy_stocks = math.floor(real_budget/((1+self.tax)*price))

        # 실제 tax는 바로 손실로 이어지니, curr_expect_balance에 적용 (소수점은 내림한다)
        tax = math.floor(num_buy_stocks * self.tax * price)
        self.curr_expect_balance -= tax
        self.curr_balance -= tax

        # 순수 주식 사는데만 쓰인 돈
        used_money = math.floor(num_buy_stocks*price)
        self.curr_balance -= used_money

        #
        if stock_code in self.stocks:
            self.stocks[stock_code]['num_stock'] += num_buy_stocks
            self.stocks[stock_code]['used_money'] += used_money
        else:
            self.stocks[stock_code] = {'num_stock':num_buy_stocks, 'used_money': used_money}

        if self.logger:
            self.logger.debug(f"\nBUY | stock_code:{stock_code}, price:{price}, time:{time}, num_stock:{num_buy_stocks}\n"
                              f"\t try:{try_budget}, real:{real_budget}, curr_balance:{self.curr_balance}, curr_expect_balance:{self.curr_expect_balance}\n"
                              f"\t tax:{tax}, used_money:{used_money}, total:({self.stocks[stock_code]['num_stock']}/{self.stocks[stock_code]['used_money']})\n")

        self.write_buy_history(stock_code, price, time, used_money)

    def sell(self, stock_code, price, time, percent=1.0):
        # 내가 그 주식 먼저 들고 있는지 확인
        if not stock_code in self.stocks:
            if self.logger:
                self.logger.debug(f"\nSELL | We don't have {stock_code}")
            return

        # 주식 들고 있으면 이제 얼만큼 팔지 정한다.
        num_stock = math.floor(self.stocks[stock_code]['num_stock'] * percent)
        used_money = math.floor(self.stocks[stock_code]['used_money'] * percent)
        self.stocks[stock_code]['num_stock'] -= num_stock
        self.stocks[stock_code]['used_money'] -= used_money

        # 판매대금
        sale_money = math.floor(price * num_stock)

        # 세금
        tax= math.floor(sale_money * self.tax)

        # 순이익
        profit = sale_money - tax - used_money

        self.curr_expect_balance += profit
        self.curr_balance += (sale_money-tax)

        if self.logger:
            self.logger.debug(f"\nSELL | stock_code:{stock_code}, price:{price}, time:{time}\n"
                              f"\t num_stock:{num_stock}, used_money:{used_money}, sale_money:{sale_money}, tax:{tax}, profit:{profit}\n"
                              f"\t curr_balance:{self.curr_balance}, curr_expect_balance:{self.curr_expect_balance}\n")

        self.write_sell_history(stock_code, price, time, sale_money)
    #
    def write_buy_history(self, stock_code, price, time, used_money):
        # tmpStr = str(price)
        tmpStr = '$b$'
        self.history.loc[time, 'BUY'] = tmpStr

    def write_sell_history(self, stock_code, price, time, sale_money):
        # tmpStr = str(price)
        tmpStr = '$s$'
        self.history.loc[time, 'SELL'] = tmpStr

    def get_history(self):
        return self.history['BUY'], self.history['SELL']

    # def logging_history(self):


