# encoding=utf-8

"""
@desc:
设置问题模板，为每个模板设置对应的SPARQL语句。demo提供如下模板：

"""
from refo import finditer, Predicate, Star, Any, Disjunction
import re

# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
prefix : <http://www.semanticweb.org/tuixiang/ontologies/mammo#>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token.decode("utf-8"))
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_feature(word_object):
        # 乳腺钼靶的影像表现有哪些
        select = u"?x"
        sparql = None

        for w in word_object:
            if w.pos == pos_mammography:
                e = u" :{mammography} :include ?o.".format(mammography=w.token.decode('utf-8'))
                    # u" ?o :征象说明 ?x.".format(mammography=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql
    @staticmethod
    def has_content(word_object):
        # 肿块的具体描述
        select = u"?o"
        sparql = None

        for w in word_object:
            if w.pos == pos_feature:
                e = u" :{feature} :征象说明 ?o.".format(feature=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def desc_by_feature(word_object):
        # 皮肤钙化是哪种特征的表现
        select = u"?x"
        sparql = None

        for w in word_object:
            if w.pos == pos_desc:
                e = u" :{desc} :describe_by ?o."\
                    u" ?o :特征说明 ?x".format(desc=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def feature_desc(word_object):
        # 钙化分布有哪些类型
        select = u"?o"
        sparql = None

        for w in word_object:
            if w.pos == pos_feature:
                e = u" :{feature} :describe ?o.".format(feature=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def desc_content(word_object):
        # 钙化弥散分布的具体表现
        select = u"?o"
        sparql = None

        for w in word_object:
            if w.pos == pos_desc:
                e = u" :{desc} :具体描述 ?o." .format(desc=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql


# TODO 定义关键词
pos_mammography = "nz"
pos_feature = "nz"
pos_desc = "nz"

mammography_entity = (W(pos=pos_mammography))
feature_entity = (W(pos=pos_feature))
desc_entity = (W(pos=pos_desc))

mammography = (W("乳腺X线摄影") | W("乳腺钼靶") | W("乳腺X光"))
feature = (W("征象") | W("特征"))
desc = (W("具体表现") | W("内容") | W("具体描述") | W("描述"))
category = (W("类型") | W("种类"))
several = (W("多少") | W("几部"))

# TODO 问题模板/匹配规则
"""
1. 乳腺X线征象有哪些? 乳腺X线摄影征象->特征
2.肿块的具体描述 or 肿块的具体描述? 特征->描述
3.皮肤钙化是哪种征象的表现? 描述:具体描述
4.钙化的分布有哪些类型? 特征:特征说明
5.弥散分布的具体表现?  描述->特征
"""
rules = [
    Rule(condition_num=2, condition=mammography_entity + Star(Any(), greedy=False) + feature + Star(Any(), greedy=False), action=QuestionSet.has_feature),
    Rule(condition_num=2, condition=feature_entity + Star(Any(), greedy=False) + desc + Star(Any(), greedy=False),
         action=QuestionSet.has_content),
    Rule(condition_num=2, condition=desc_entity + Star(Any(), greedy=False) + feature + Star(Any(), greedy=False),
         action=QuestionSet.desc_by_feature),
    Rule(condition_num=2, condition=feature_entity + Star(Any(), greedy=False) + category + Star(Any(), greedy=False),
         action=QuestionSet.feature_desc),
    Rule(condition_num=2, condition=desc_entity + Star(Any(), greedy=False) + desc + Star(Any(), greedy=False),
         action=QuestionSet.desc_content),

]  # W()可以简单的把它理解为re中compile后的match，只不过多个W()间出现的顺序可以变化, 通过多个定制的W()和Star(Any(), greedy=False)(相当于.*?)这种通配符的组合