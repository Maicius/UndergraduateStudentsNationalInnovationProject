import pandas as pd
from USNIP import USNIP
if __name__ == '__main__':
    usnip = USNIP()
    # 获取数据
    _2015_data = pd.read_excel('2015.xls', header=None)
    usnip._2015_keyword = pd.DataFrame(usnip.calculate_keyword(_2015_data.iloc[3:, 3:4])).reset_index()

    _2016_data = pd.read_excel('2016.xlsx', header=None, sheet_name='信息表')
    usnip._2016_keyword = pd.DataFrame(usnip.calculate_keyword(_2016_data.iloc[3:, 5:6])).reset_index()

    _2017_data = pd.read_excel('2017.xlsx', header=None)
    usnip._2017_keyword = pd.DataFrame(usnip.calculate_keyword(_2017_data.iloc[3:, 3:4])).reset_index()

    # 重置列名
    usnip.reset_index_name()
    usnip.calculate_rank_diff()

    pass