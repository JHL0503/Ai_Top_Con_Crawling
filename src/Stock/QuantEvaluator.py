# df를 받아서
# 거래당 승률,



import logging
import math
import pandas as pd
import datetime

class QuantEvaluator:

    def __init__(self, strategy_name, logger:logging=None):
        self.strategy_name = strategy_name
        self.logger = logger
        self.data = list()
        self.transaction_history = None

    def put_transaction(self, date:datetime, balance):
        self.data.append({'date': date, 'balance': balance})

    def put_transaction_history(self, transaction_history):
        self.transaction_history = transaction_history

    def _change_time_type(self, date):
        if(type(date) == pd.Timestamp):
            return date.to_pydatetime()
        else:
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    def _cal_win_rate_per_transaction(self, df):
        total_cnt = 0
        win_cnt = 0
        for i in range(len(df)):
            if i==0:
                continue

            prev_item = df.iloc[i - 1]
            curr_item = df.iloc[i]

            if(prev_item['balance'] < curr_item['balance']):
                win_cnt += 1

            total_cnt += 1
        return round(win_cnt/total_cnt,4)

    def _cal_avg_profit_per_trans(self, df):
        init_balance = df.iloc[0]['balance']
        final_balance = df.iloc[-1]['balance']
        total_earning_ratio = final_balance / init_balance
        num_trans = len(df)-1
        avg_profit_per_trans = round(total_earning_ratio ** (1/num_trans), 4)
        return round((avg_profit_per_trans - 1),4)


    def _cal_avg_profit_per_years(self, df):
        init_balance = df.iloc[0]['balance']
        final_balance = df.iloc[-1]['balance']
        total_earning_ratio = final_balance / init_balance

        init_date = self._change_time_type(df.iloc[0]['date'])
        fianl_date = self._change_time_type(df.iloc[-1]['date'])
        day_difference = (fianl_date - init_date).days
        num_years = day_difference / 365
        if(num_years < 1):
            return -1


        avg_profit_per_years = total_earning_ratio ** (1/num_years)
        return round((avg_profit_per_years - 1),4)


    def _cal_MDD(self, df):
        max_val = 0
        max_val_date = None
        max_MDD = 1
        max_recover_day = 0
        MDD_df = pd.Series(index=df.index)
        for i in range(len(df)):
            curr_item = df.iloc[i]
            if curr_item['balance'] >= max_val:
                max_val = curr_item['balance']

                if max_val_date == None:
                    prev_max_val_date = self._change_time_type(curr_item['date'])
                else:
                    prev_max_val_date = max_val_date
                max_val_date = self._change_time_type(curr_item['date'])
                recovery_time = (max_val_date - prev_max_val_date).days

                if max_recover_day <= recovery_time:
                    max_recover_day = recovery_time

            mdd = (1- ((max_val - curr_item['balance']) / max_val))
            if mdd <= max_MDD:
                max_MDD = mdd

            MDD_df.iloc[i] = round(mdd,4)

        self.transaction_history['MDD'] = MDD_df
        return round(1-max_MDD,4), max_recover_day


    def evaluate(self):
        if len(self.data) != 0:
            self.transaction_history = pd.DataFrame(self.data)
        elif self.transaction_history == None:
            if self.logger:
                self.logger.error(f"QuantEvaluator: Nothing to do!")
            return None, None


        # 거래당 승률, 거래당 수익률
        statics = dict()
        statics['name'] = self.strategy_name
        statics['total_earning_ratio'] = self.transaction_history.iloc[-1]['balance'] / self.transaction_history.iloc[0]['balance']
        statics['win_rate_per_trans'] = self._cal_win_rate_per_transaction(self.transaction_history)
        statics['avg_profit_per_trans'] = self._cal_avg_profit_per_trans(self.transaction_history)
        statics['avg_profit_per_years'] = self._cal_avg_profit_per_years(self.transaction_history)
        statics['max_MDD'], statics['max_recover_day'] = self._cal_MDD(self.transaction_history)

        return self.transaction_history, statics


