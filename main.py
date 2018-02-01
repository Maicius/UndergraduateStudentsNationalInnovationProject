import pandas as pd
from USNIP import USNIP

if __name__ == '__main__':
    usnip = USNIP()
    # 获取数据
    _2015_data = pd.read_excel('2015.xls', header=None)
    usnip._2015_keyword = usnip.calculate_keyword(_2015_data.iloc[3:, 3:4])

    _2016_data = pd.read_excel('2016.xlsx', header=None, sheet_name='信息表')
    usnip._2016_keyword = usnip.calculate_keyword(_2016_data.iloc[3:, 5:6])

    _2017_data = pd.read_excel('2017.xlsx', header=None)
    usnip._2017_keyword = usnip.calculate_keyword(_2017_data.iloc[3:, 3:4])

    _2016_2017_diff_df, _2015_2016_diff_df = usnip.calculate_rank_diff()
    print(_2016_2017_diff_df)
    _2016_2017_diff_df.columns = ['排名', '关键字', '2016 - 2017年增加值']
    _2015_2016_diff_df.columns = ['排名', '关键字', '2015 - 2016年增加值']
    _2015_2016_diff_df.to_excel('result/2015-2016_diff.xlsx')
    _2016_2017_diff_df.to_excel('result/2016-2017_diff.xlsx')
    print('finish')