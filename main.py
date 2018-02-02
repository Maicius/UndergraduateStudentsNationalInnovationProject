import pandas as pd
from USNIP import USNIP


def get_keyword_diff():
    # 统计与关键词有关的信息
    usnip._2015_keyword = usnip.calculate_keyword(_2015_data.iloc[3:, 3:4])
    usnip._2016_keyword = usnip.calculate_keyword(_2016_data.iloc[3:, 5:6])
    usnip._2017_keyword = usnip.calculate_keyword(_2017_data.iloc[3:, 3:4])
    _2016_2017_diff_df, _2015_2016_diff_df = usnip.calculate_rank_diff()
    print(_2016_2017_diff_df)
    _2016_2017_diff_df.columns = ['排名', '关键字', '2016 - 2017年增加值']
    _2015_2016_diff_df.columns = ['排名', '关键字', '2015 - 2016年增加值']
    _2015_2016_diff_df.to_excel('result/2015-2016_diff.xlsx')
    _2016_2017_diff_df.to_excel('result/2016-2017_diff.xlsx')


def get_total_key_word():
    usnip.create_total_df()


def get_avg_people():
    usnip._2015_avg_people = usnip.calculate_avg_people(_2015_data[[1, 7]].loc[3:])
    usnip._2016_avg_people = usnip.calculate_avg_people(_2016_data[[3, 9]].loc[3:])
    usnip._2017_avg_people = usnip.calculate_avg_people(_2017_data[[1, 7]].loc[3:])
    usnip.calculate_avg_people(usnip._2015_avg_people)
    usnip.calculate_avg_people(usnip._2016_avg_people)
    usnip.calculate_avg_people(usnip._2017_avg_people)
    usnip.create_all_avg_people_df()


def draw_word_cloud():
    usnip.multiply_ten()
    usnip.drawWordCloud(usnip._2015_keyword, 'result/2015_word_cloud.jpg')
    usnip.drawWordCloud(usnip._2016_keyword, 'result/2016_word_cloud.jpg')
    usnip.drawWordCloud(usnip._2017_keyword, 'result/2017_word_cloud.jpg')


if __name__ == '__main__':
    usnip = USNIP()
    # 获取数据
    _2015_data = pd.read_excel('2015.xls', header=None)
    _2016_data = pd.read_excel('2016.xlsx', header=None, sheet_name='信息表')
    _2017_data = pd.read_excel('2017.xlsx', header=None)

    # get_keyword_diff()
    # get_total_key_word()
    # draw_word_cloud()
    get_avg_people()
    # 计算平均项目人数


    print('finish')
