import os
import pandas as pd
import time

CURR_PATH = os.path.dirname(__file__)
CURR_DAY = time.strftime("%Y%m%d")
print(CURR_DAY)
CURR_MONTH = time.strftime("%Y%m")
print(CURR_MONTH)

class YingShe():
    def __init__(self):
        self.file = os.path.join(CURR_PATH, '../data/周映射表.xlsx')

    def create_diction(self):
        db = pd.read_excel(self.file,sheet_name=CURR_MONTH)
        dict_yingshe = {}
        for item in db:
            period = item
            week_day = list(db[item])
            dict_yingshe[period] = week_day
        return dict_yingshe

    def get_week(self):
        res = self.create_diction()
        for key,values in res.items():
            for value in values:
                if value == int(CURR_DAY):
                    print('key',key)
                    return key

    def get_period(self):
        period_id = self.get_week()
        global CURR_MONTH # 全局变量可以直接使用，但是想改动全局变量，必须在方法中先声明。
        if str(period_id)[0] == 'W':
            pass
        else:
            CURR_MONTH = period_id
            period_id = self.get_week()
        period_value = str(period_id) + '_' + CURR_DAY
        return period_id,period_value


if __name__ == '__main__':
    res = YingShe()
    x,y = res.get_period()
    print(x,y)