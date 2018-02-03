# coding=utf-8
import jieba
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from scipy.misc import imread
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

def count_frequency(data_arr):
    _keyword_dict = {}
    for word in data_arr:
        if word not in _keyword_dict:
            _keyword_dict[word] = 1
        else:
            _keyword_dict[word] += 1
    return _keyword_dict


class USNIP(object):
    def __init__(self):
        self._2015_keyword = {}
        self._2016_keyword = {}
        self._2017_keyword = {}
        self._2015_avg_people_df = []
        self._2016_avg_people_df = []
        self._2017_avg_people_df = []

        self.waste_words = "基于 研究 技术 方法 理论 为例 实验 影响 模拟 作用 应用 工程 探究 探索 浅析 机制 坚定 分析 调研 构建 特征 " \
                           "设计 方案 新型 及其 系统 公司 组织 平台 用于 对策 不同 使用 调查 合作 辅助 我国 地区 " \
                           "制备 大学生 开发 合成 实现 检测 中国 高校 研制 优化 服务 有限 项目 发展 装置 问题 现状 一种 结构 模型 性能 " \
                           "模式 有限公司 试验 比较 推广 利用 特性 因素 机理 建设 算法 背景 现状及 表达 快速 吸附"
        self.generate_waste_words_array()

    def calculate_keyword(self, data):
        project_names = data.sum(axis=0).values[0]
        # 载入自定义字典
        jieba.load_userdict("userdict.txt")
        _keyword = list(jieba.cut(project_names, cut_all=False))
        _keyword = filter(self.remove_waste, _keyword)
        _keyword_dict = count_frequency(_keyword)
        return _keyword_dict

    def generate_waste_words_array(self):
        self.waste_words = set(self.waste_words.split(' '))

    def remove_waste(self, word):
        if word in self.waste_words or len(word) < 2:
            return ''
        return word

    def calculate_rank_diff(self):
        _2016_2017_diff_dict = {}
        for word in self._2017_keyword:
            if word in self._2016_keyword:
                _2016_2017_diff_dict[word] = self._2017_keyword[word] - self._2016_keyword[word]
            else:
                _2016_2017_diff_dict[word] = self._2017_keyword[word]
        _2015_2016_diff_dict = {}
        for word in self._2016_keyword:
            if word in self._2015_keyword:
                _2015_2016_diff_dict[word] = self._2016_keyword[word] - self._2015_keyword[word]
            else:
                _2015_2016_diff_dict[word] = self._2016_keyword[word]
        _2016_2017_diff_dict = pd.DataFrame(sorted(_2016_2017_diff_dict.items(), key=lambda x: x[1], reverse=True),
                                            index=None).reset_index()
        _2015_2016_diff_dict = pd.DataFrame(sorted(_2015_2016_diff_dict.items(), key=lambda x: x[1], reverse=True),
                                            index=None).reset_index()

        return _2016_2017_diff_dict, _2015_2016_diff_dict

    def create_total_df(self):
        _2015_df = pd.DataFrame(sorted(self._2015_keyword.items(), key=lambda x: x[1], reverse=True))
        _2015_df.columns = ['2015关键字', '2015数量']
        _2016_df = pd.DataFrame(sorted(self._2016_keyword.items(), key=lambda x: x[1], reverse=True))
        _2016_df.columns = ['2016关键字', '2016数量']
        _2017_df = pd.DataFrame(sorted(self._2017_keyword.items(), key=lambda x: x[1], reverse=True))
        _2017_df.columns = ['2017关键字', '2017数量']
        all_year_df = pd.concat([_2015_df, _2016_df], axis=1)
        all_year_df = pd.concat([all_year_df, _2017_df], axis=1)
        all_year_df = all_year_df.iloc[0:100]
        all_year_df['2015数量'].astype(int)
        all_year_df['2016数量'].astype(int)
        print(all_year_df)
        all_year_df.to_excel('result/关键字表.xlsx')
        print("Finish")

    def create_all_avg_people_df_by_univer(self):
        self._2015_avg_people_df.columns = ['2015高校', '2015平均人数']
        self._2016_avg_people_df.columns = ['2016高校', '2016平均人数']
        self._2017_avg_people_df.columns = ['2017高校', '2017平均人数']
        all_year_df = pd.concat([self._2015_avg_people_df, self._2016_avg_people_df, self._2017_avg_people_df], axis=1)
        all_year_df.to_excel('result/平均人数表.xlsx')
        print('Finish')

    def create_all_avg_people_df_by_num(self):
        self._2015_avg_people_df.columns = ['2015项目参与人数', '2015数量']
        self._2016_avg_people_df.columns = ['2016项目参与人数', '2016数量']
        self._2017_avg_people_df.columns = ['2017项目参与人数', '2017数量']
        all_year_df = pd.concat([self._2015_avg_people_df, self._2016_avg_people_df, self._2017_avg_people_df], axis=1)
        all_year_df.to_excel('result/项目参与人数表.xlsx')
        print('Finish')
        return all_year_df

    def drawWordCloud(self, word_text, filename):
        mask = imread('pic.png')
        my_wordcloud = WordCloud(
            background_color='white',  # 设置背景颜色
            mask=mask,  # 设置背景图片
            max_words=5000,  # 设置最大显示的字数
            stopwords=STOPWORDS,  # 设置停用词
            font_path='/System/Library/Fonts/Hiragino Sans GB.ttc',  # 设置字体格式，如不设置显示不了中文
            max_font_size=50,  # 设置字体最大值
            random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
            scale=1.5
        ).fit_words(word_text)
        image_colors = ImageColorGenerator(mask)
        my_wordcloud.recolor(color_func=image_colors)
        # 保存图片
        my_wordcloud.to_file(filename=filename)
        # 以下代码显示图片
        # plt.imshow(my_wordcloud)
        # plt.axis("off")
        # plt.show()

    def multiply_ten(self):
        for index, value in self._2015_keyword.items():
            self._2015_keyword[index] = value ** 2

        for index, value in self._2016_keyword.items():
            self._2016_keyword[index] = value ** 2

        for index, value in self._2017_keyword.items():
            self._2017_keyword[index] = value ** 2

    def calculate_avg_people_by_univer(self, data):
        university_tuple = []
        data.columns = ['university', 'num']
        unique_university = pd.unique(data['university'].values)
        for university in unique_university:
            avg_people = data[data.university == university]['num'].astype(int).mean()
            university_tuple.append((university, round(avg_people, 0)))
        university_df = pd.DataFrame(university_tuple)
        university_df.columns = ['大学', '平均人数']
        university_df.sort_values(by='平均人数', inplace=True, ascending=True)
        university_df = university_df.reset_index().drop(['index'], axis=1)
        print(university_df)
        return university_df

    def calculate_avg_people_by_num(self, data):
        data['val'] = 1
        avg_people_tuple = []
        data.columns = ['num', 'val']
        data.astype(int, copy=False)
        unique_num = pd.unique(data['num'].values)
        for num in unique_num:
            avg_num = data[data.num == num]['val'].sum(axis=0)
            avg_people_tuple.append((num, avg_num))
        avg_people_df = pd.DataFrame(avg_people_tuple)
        avg_people_df.columns = ['参数人数', '项目数量']
        avg_people_df.sort_values(by='项目数量', inplace=True, ascending=False)
        avg_people_df = avg_people_df.reset_index().drop(['index'], axis=1)
        print(avg_people_df)
        return avg_people_df

    def draw_picture(self, num_data):
        num_data.columns = ['_2015_people', '_2015_num', '_2016_people', '_2016_num', '_2017_people', '_2017_num']
        num_data_2015_df = self.groupy_by_avg_people(num_data, num_data._2015_people, '_2015_num')
        num_data_2016_df = self.groupy_by_avg_people(num_data, num_data._2016_people, '_2016_num')
        num_data_2017_df = self.groupy_by_avg_people(num_data, num_data._2017_people.astype(int), '_2017_num')
        num_data_df = pd.concat([num_data_2015_df, num_data_2016_df, num_data_2017_df], axis=0).astype(int)
        num_data_df.columns = ['less_2', '_3_5', 'more_5', 'sum_val']
        num_data_df.to_excel('result/项目参与人数统计表.xlsx')
        self.do_draw_mat(data_df=num_data_df)

    def do_draw_mat(self, data_df):
        size = 3
        custom_font = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/Hiragino Sans GB.ttc')
        a = data_df['less_2'].values
        b = data_df['_3_5'].values
        c = data_df['more_5'].values
        x = np.arange(size)
        total_width, n = 0.8, 3  # 有多少个类型，只需更改n即可
        width = total_width / n
        x = x - (total_width - width) / 2
        year = ['2015', '2016', '2017']
        plt.title('近三年部属高校大创项目人数统计图', fontproperties=custom_font)
        plt.bar(x, a, width=width, label='小于等于2人', color='#0072BC')
        plt.bar(x + width, b, width=width, label='3至5人', color='#ED1C24')
        plt.bar(x + 2 * width, c, width=width, label='大于5人')
        for i in range(len(a)):
            plt.text(x[i] + 0.5 * width, a[i] + 0.05, a[i], ha='center', va='bottom')
            plt.text(x[i] + 1.5 * width, b[i] + 0.05, b[i], ha='center', va='bottom')
            plt.text(x[i] + 2.5 * width, c[i] + 0.05, c[i], ha='center', va='bottom')
        plt.xticks(x + 1.5 * width, year, fontproperties=custom_font)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5, prop=custom_font)
        plt.show()

    def groupy_by_avg_people(self, num_data, row_num, col_num):
        small = num_data[row_num <= 2][[col_num]].sum(axis=0)
        middle = num_data[row_num <= 5][[col_num]].sum(axis=0) - small
        big = num_data[row_num > 5][[col_num]].sum(axis=0)
        print(small, middle, big)
        num_data_df = pd.concat([small, middle, big], axis=1).astype(int)
        num_data_df['sum_val'] = num_data_df.sum(axis=1)
        return num_data_df

    def calculate_money(self, data):
        university_tuple = []
        data.columns = ['university', 'money']
        unique_university = pd.unique(data['university'].values)
        for university in unique_university:
            avg_people = data[data.university == university]['money'].astype(int).mean()
            university_tuple.append((university, round(avg_people, 0)))
        university_df = pd.DataFrame(university_tuple)
        university_df.columns = ['大学', '平均人数']
        university_df.sort_values(by='平均人数', inplace=True, ascending=True)
        university_df = university_df.reset_index().drop(['index'], axis=1)
        print(university_df)
        return university_df