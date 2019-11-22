# -*- coding: utf-8 -*-

# NER预料train.txt所在的路径
dir = "../CRF_TEST"

with open("%s/train.txt" % dir, "r") as f:
    sents = [line.strip() for line in f.readlines()]

# 训练集与测试集的比例为9:1
RATIO = 0.9
train_num = int((len(sents)//3)*RATIO)

# 将文件分为训练集与测试集
with open("%s/NER_train.data" % dir, "w") as g:
    for i in range(train_num):
        words = sents[3*i].split('\t')
        postags = sents[3*i+1].split('\t')
        tags = sents[3*i+2].split('\t')
        for word, postag, tag in zip(words, postags, tags):
            g.write(word+' '+postag+' '+tag+'\n')
        g.write('\n')

with open("%s/NER_test.data" % dir, "w") as h:
    for i in range(train_num+1, len(sents)//3):
        words = sents[3*i].split('\t')
        postags = sents[3*i+1].split('\t')
        tags = sents[3*i+2].split('\t')
        for word, postag, tag in zip(words, postags, tags):
            h.write(word+' '+postag+' '+tag+'\n')
        h.write('\n')

print('OK!')