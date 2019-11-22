# -*- coding: utf-8 -*-

# pip install graphviz
# yum install xdg-utils
import os
import jieba
from pyltp import  Postagger, Parser

sent = '2018年7月26日，华为创始人任正非向5G极化码（Polar码）之父埃尔达尔教授举行颁奖仪式，表彰其对于通信领域做出的贡献。'

jieba.add_word('Polar码')
jieba.add_word('5G极化码')
jieba.add_word('埃尔达尔')
jieba.add_word('之父')
words = list(jieba.cut(sent))

print(words)

# 词性标注
pos_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/pos.model')
postagger = Postagger()
postagger.load(pos_model_path)
postags = postagger.postag(words)

# 依存句法分析
par_model_path = os.path.join(os.path.dirname(__file__), 'ltp_data_v3.4.0/parser.model')
parser = Parser()
parser.load(par_model_path)
arcs = parser.parse(words, postags)

rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
relation = [arc.relation for arc in arcs]  # 提取依存关系
heads = ['Root' if id == 0 else words[id-1] for id in rely_id]  # 匹配依存父节点词语

for i in range(len(words)):
    print(relation[i] + '(' + words[i] + ', ' + heads[i] + ')')


# 可视化
from graphviz import Digraph
g = Digraph('测试图片')
g.node(name='Root')
for word in words:
    g.node(name=word)

for i in range(len(words)):
    if relation[i] not in ['HED']:
        g.edge(words[i], heads[i], label=relation[i])
    else:
        if heads[i] == 'Root':
            g.edge(words[i], 'Root', label=relation[i])
        else:
            g.edge(heads[i], 'Root', label=relation[i])

g.view()