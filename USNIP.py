# coding=utf-8
import jieba
import numpy as np
jieba.load_userdict("userdict.txt")


def count_frequency(data_arr):
    _keyword_dict = {}
    for word in data_arr:
        if word not in data_arr:
            _keyword_dict[word] = 1
        else:
            _keyword_dict[word] += 1
    return _keyword_dict


class USNIP(object):
    def __init__(self):
        self._2015_data = []
        self._2015_keyword = []
        self._2016_keyword = []
        self._2017_keyword = []
        self.waste_words = "基于 研究 技术 方法 理论 为例 实验 影响 模拟 作用 应用 工程 探究 探索 浅析 机制 坚定 分析 调研 构建 特征 " \
                           "设计 方案 新型 及其 系统 公司 组织 平台 用于 对策 不同 使用 调查 合作 辅助 我国 地区 的 与 -"
        self._2015_keyword_dict = {}

    def calculate_keyword(self, data):
        project_names = data.sum(axis=0).values[0]
        self.generate_waste_words_array()
        for item in self.waste_words:
            project_names = project_names.replace(item, '')
        project_names = project_names.replace(' ', '')
        self._2015_keyword = list(jieba.cut(project_names, cut_all=False))
        print(self._2015_keyword)
        self._2015_keyword_dict = count_frequency(self._2015_keyword)
        print(sorted(self._2015_keyword_dict, key=lambda x:x[1], reverse=True))

    def generate_waste_words_array(self):
        self.waste_words = self.waste_words.split(' ')
