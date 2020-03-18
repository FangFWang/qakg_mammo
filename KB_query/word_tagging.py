# encoding=utf-8
# @desc: 定义Word类的结构；定义Tagger类，实现自然语言转为Word对象的方法。

import jieba
import jieba.posseg as pseg

class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos

class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)  # 开发者可以指定自己自定义的词典，以便包含 jieba 词库里没有的词。虽然 jieba 有新词识别能力，但是自行添加新词可以保证更高的正确率

    @staticmethod
    def get_word_objects(sentence):
        # 把自然语言转为Word对象
        return [Word(word.encode('utf-8'), tag) for word, tag in pseg.cut(sentence)]  # 词性标注

# TODO 用于测试
if __name__ == '__main__':
    tagger = Tagger(['./external_dict/mammo.txt'])
    while True:
        # s = input()
        s = '钙化分布有哪些类型'
        print(tagger.get_word_objects(s))
        for i in tagger.get_word_objects(s):
            print (i.token.decode(), i.pos)
            print ('==================')
