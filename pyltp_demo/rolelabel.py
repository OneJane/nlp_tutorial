# 语义角色标注
# -*- coding: utf-8 -*-

import os
from pyltp import Segmentor, Postagger, Parser, SementicRoleLabeller

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

# 依存句法分析
par_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/parser.model')  # 模型路径，模型名称为`parser.model`

parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型
arcs = parser.parse(words, postags)  # 句法分析

# 语义角色标注
srl_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/pisrl.model')  # 语义角色标注模型目录路径
labeller = SementicRoleLabeller() # 初始化实例
labeller.load(srl_model_path)  # 加载模型
roles = labeller.label(words, postags, arcs)  # 语义角色标注

# 打印结果
for role in roles:
    print(words[role.index], end=' ')
    print(role.index, "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

# 释放模型
segmentor.release()
postagger.release()
parser.release()
labeller.release()