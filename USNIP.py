# coding=utf-8
import jieba
import pandas as pd

jieba.load_userdict("userdict.txt")


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
        self.waste_words = "基于 研究 技术 方法 理论 为例 实验 影响 模拟 作用 应用 工程 探究 探索 浅析 机制 坚定 分析 调研 构建 特征 " \
                           "设计 方案 新型 及其 系统 公司 组织 平台 用于 对策 不同 使用 调查 合作 辅助 我国 地区 " \
                           "制备 大学生 开发 合成 实现 检测 中国 高校 研制 优化 服务 有限 项目 发展 装置 问题 现状 一种 结构 模型 性能 " \
                           "模式 有限公司 试验 比较 推广 利用 特性 因素 机理 建设 算法 背景 现状及 表达 快速 吸附"
        self._2015_keyword_dict = {}
        self.generate_waste_words_array()

    def calculate_keyword(self, data):
        project_names = data.sum(axis=0).values[0]

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
        all_year_df.fillna(0)
        all_year_df['2015数量'].astype(int)
        all_year_df['2016数量'].astype(int)
        print(all_year_df)
        pass
