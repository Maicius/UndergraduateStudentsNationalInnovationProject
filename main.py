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


def get_avg_people_by_univer():
    usnip._2015_avg_people_df = usnip.calculate_avg_people_by_univer(_2015_data[[1, 7]].loc[3:])
    usnip._2016_avg_people_df = usnip.calculate_avg_people_by_univer(_2016_data[[3, 9]].loc[3:])
    usnip._2017_avg_people_df = usnip.calculate_avg_people_by_univer(_2017_data[[1, 7]].loc[3:])
    usnip.create_all_avg_people_df_by_univer()


def get_avg_people_by_num():
    usnip._2015_avg_people_df = usnip.calculate_avg_people_by_num(_2015_data[[7]].loc[3:])
    usnip._2016_avg_people_df = usnip.calculate_avg_people_by_num(_2016_data[[9]].loc[3:])
    usnip._2017_avg_people_df = usnip.calculate_avg_people_by_num(_2017_data[[7]].loc[3:])
    num_data = usnip.create_all_avg_people_df_by_num()
    usnip.draw_picture(num_data)


def draw_word_cloud():
    usnip.multiply_ten()
    usnip.drawWordCloud(usnip._2015_keyword, 'result/2015_word_cloud.jpg')
    usnip.drawWordCloud(usnip._2016_keyword, 'result/2016_word_cloud.jpg')
    usnip.drawWordCloud(usnip._2017_keyword, 'result/2017_word_cloud.jpg')


def get_total_money():
    _2015_df = usnip.calculate_money(_2015_data[[1, 11]].loc[3:])
    _2016_df = usnip.calculate_money(_2016_data[[3, 15]].loc[3:])
    total_df = pd.concat([_2015_df, _2016_df], axis=1)
    total_df.columns = ['2015高校', '2015经费', '2016高校', '2016经费']
    print(total_df)
    total_df.to_excel('2015-2016国家级大创经费情况.xlsx')

    sum_money_df = pd.DataFrame(total_df.sum(axis=0))
    sum_money_df.drop(['2015高校', '2016高校'], axis=0, inplace=True)
    sum_money_df.to_excel('2015-2016国家级大创总经费.xlsx')
    print(sum_money_df.values)
    usnip.draw_simple_bar(sum_money_df.values)
    pass


if __name__ == '__main__':
    usnip = USNIP()
    # 获取数据
    _2015_data = pd.read_excel('raw_data/2015.xls', header=None)
    _2016_data = pd.read_excel('raw_data/2016.xlsx', header=None, sheet_name='信息表')
    _2017_data = pd.read_excel('raw_data/2017.xlsx', header=None)

    # 计算关键字
    # get_keyword_diff()
    # get_total_key_word()
    # 绘制词云
    # draw_word_cloud()
    # 计算项目平均参与人数
    get_avg_people_by_univer()

    # get_avg_people_by_num()

    get_total_money()
    print('finish')
