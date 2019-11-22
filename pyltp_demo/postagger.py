# -*- coding: utf-8 -*-
# 词性标注
import os
from pyltp import Segmentor, Postagger

# 分词
cws_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/cws.model')  # 分词模型路径，模型名称为`cws.model`
lexicon_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/lexicon.txt')  # 参数lexicon是自定义词典的文件路径

segmentor = Segmentor()
segmentor.load_with_lexicon(cws_model_path, lexicon_path)

sent = '据韩联社12月28日反映，美国防部发言人杰夫·莫莱尔27日表示，美国防部长盖茨将于2011年1月14日访问韩国。'
words = segmentor.segment(sent)  # 分词

# 词性标注
pos_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/pos.model')  # 词性标注模型路径，模型名称为`pos.model`

postagger = Postagger()  # 初始化实例
postagger.load(pos_model_path)  # 加载模型
postags = postagger.postag(words)  # 词性标注

for word, postag in zip(words, postags):
    print(word, postag)

# 释放模型
segmentor.release()
postagger.release()
# https://ltp.readthedocs.io/zh_CN/latest/appendix.html