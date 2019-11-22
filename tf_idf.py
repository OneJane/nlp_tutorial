"""
tf-idf 原理：tfidf = tf*idf tf是词频(Term Frequency)，idf为逆向文件频率(Inverse Document Frequency)。
tf为词频，即一个词语在文档中的出现频率，假设一个词语在整个文档中出现了i次，而整个文档有N个词语，则tf的值为i/N.
idf为逆向文件频率，假设整个文档有n篇文章，而一个词语在k篇文章中出现，则idf值为log(n/k)
"""
import nltk
import math
import string
from nltk.corpus import stopwords  # 停用词
from collections import Counter  # 计数
from gensim import corpora, models, matutils

# 文本预处理
text1 = """
Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. 
Unqualified, the word football is understood to refer to whichever form of football is the most popular 
in the regional context in which the word appears. Sports commonly called football in certain places 
include association football (known as soccer in some countries); gridiron football (specifically American 
football or Canadian football); Australian rules football; rugby football (either rugby league or rugby union); 
and Gaelic football. These different variations of football are known as football codes.
"""

text2 = """
Basketball is a team sport in which two teams of five players, opposing one another on a rectangular court, 
compete with the primary objective of shooting a basketball (approximately 9.4 inches (24 cm) in diameter) 
through the defender's hoop (a basket 18 inches (46 cm) in diameter mounted 10 feet (3.048 m) high to a backboard 
at each end of the court) while preventing the opposing team from shooting through their own hoop. A field goal is 
worth two points, unless made from behind the three-point line, when it is worth three. After a foul, timed play stops 
and the player fouled or designated to shoot a technical foul is given one or more one-point free throws. The team with 
the most points at the end of the game wins, but if regulation play expires with the score tied, an additional period 
of play (overtime) is mandated.
"""

text3 = """
Volleyball, game played by two teams, usually of six players on a side, in which the players use their hands to bat a 
ball back and forth over a high net, trying to make the ball touch the court within the opponents’ playing area before 
it can be returned. To prevent this a player on the opposing team bats the ball up and toward a teammate before it touches 
the court surface—that teammate may then volley it back across the net or bat it to a third teammate who volleys it across 
the net. A team is allowed only three touches of the ball before it must be returned over the net.
"""


# 文本预处理 text文件分句，分词，并去掉标点
def get_tokens(text):
    text = text.replace('\n', '')
    sents = nltk.sent_tokenize(text)  # 分句
    tokens = []
    for sent in sents:
        for word in nltk.word_tokenize(sent):  # 分词
            if word not in string.punctuation:  # 去掉标点
                tokens.append(word)
    return tokens


# 对原始的text文件去掉停用词 生成count字典，即每个单词的出现次数
def make_count(text):
    tokens = get_tokens(text)
    filtered = [w for w in tokens if not w in stopwords.words('english')]  # 去掉停用词
    count = Counter(filtered)
    return count


print(make_count(text3))

"""
 用gensim中的已实现的TF-IDF模型，来输出每篇文章中TF-IDF排名前三的单词及它们的tfidf值
"""
from nltk.corpus import stopwords  # 停用词
from gensim import corpora, models, matutils


# training by gensim's Ifidf Model
def get_words(text):
    tokens = get_tokens(text)
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    return filtered


# get text
count1, count2, count3 = get_words(text1), get_words(text2), get_words(text3)
countlist = [count1, count2, count3]
# training by TfidfModel in gensim
dictionary = corpora.Dictionary(countlist)
new_dict = {v: k for k, v in dictionary.token2id.items()}
corpus2 = [dictionary.doc2bow(count) for count in countlist]
tfidf2 = models.TfidfModel(corpus2)
corpus_tfidf = tfidf2[corpus2]

# 关于足球的文章中提取了football, rugby关键词，关于篮球的文章中提取了plat, cm关键词，关于排球的文章中提取了net, teammate关键词
print("\nTraining by gensim Tfidf Model.......\n")
for i, doc in enumerate(corpus_tfidf):
    print("Top words in document %d" % (i + 1))
    sorted_words = sorted(doc, key=lambda x: x[1], reverse=True)  # type=list
    for num, score in sorted_words[:3]:
        print("    Word: %s, TF-IDF: %s" % (new_dict[num], round(score, 5)))

"""
手动实现tf-idf
"""

import numpy as np


# 计算tf
def tf(word, count):
    return count[word] / sum(count.values())


# 计算count_list有多少个文件包含word
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


# 计算idf
def idf(word, count_list):
    return math.log2(len(count_list) / (n_containing(word, count_list)))  # 对数以2为底


# 计算tf-idf
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


# 对向量做规范化, normalize
def unitvec(sorted_words):
    lst = [item[1] for item in sorted_words]
    L2Norm = math.sqrt(sum(np.array(lst) * np.array(lst)))
    unit_vector = [(item[0], item[1] / L2Norm) for item in sorted_words]
    return unit_vector


# TF-IDF测试
count1, count2, count3 = make_count(text1), make_count(text2), make_count(text3)
countlist = [count1, count2, count3]
print("Training by original algorithm......\n")
for i, count in enumerate(countlist):
    print("Top words in document %d" % (i + 1))
    scores = {word: tfidf(word, count, countlist) for word in count}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)  # type=list
    sorted_words = unitvec(sorted_words)  # normalize
    for word, score in sorted_words[:3]:
        print("    Word: %s, TF-IDF: %s" % (word, round(score, 5)))

"""
用gensim使用tf-idf模型计算两个句子的相似度
"""
from gensim import corpora, models, similarities
import logging
from collections import defaultdict
import jieba

# 设置日志
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 准备数据：现有8条文本数据，将8条文本数据放入到list中
documents = ["1)键盘是用于操作设备运行的一种指令和数据输入装置，也指经过系统安排操作一台机器或设备的一组功能键（如打字机、电脑键盘）",
             "2)鼠标称呼应该是“鼠标器”，英文名“Mouse”，鼠标的使用是为了使计算机的操作更加简便快捷，来代替键盘那繁琐的指令。",
             "3)中央处理器（CPU，Central Processing Unit）是一块超大规模的集成电路，是一台计算机的运算核心（Core）和控制核心（ Control Unit）。",
             "4)硬盘是电脑主要的存储媒介之一，由一个或者多个铝制或者玻璃制的碟片组成。碟片外覆盖有铁磁性材料。",
             "5)内存(Memory)也被称为内存储器，其作用是用于暂时存放CPU中的运算数据，以及与硬盘等外部存储器交换的数据。",
             "6)显示器（display）通常也被称为监视器。显示器是属于电脑的I/O设备，即输入输出设备。它是一种将一定的电子文件通过特定的传输设备显示到屏幕上再反射到人眼的显示工具。",
             "7)显卡（Video card，Graphics card）全称显示接口卡，又称显示适配器，是计算机最基本配置、最重要的配件之一。",
             "8)cache高速缓冲存储器一种特殊的存储器子系统，其中复制了频繁使用的数据以利于快速访问。"]
# 待比较的文档
new_doc = "内存又称主存，是CPU能直接寻址的存储空间，由半导体器件制成。"

# 1.文本预处理：中文分词，去除停用词
print('1.文本预处理：中文分词，去除停用词')
# 获取停用词
stopwords = set()
file = open("stopwords.txt", 'r', encoding='UTF-8')
for line in file:
    stopwords.add(line.strip())
file.close()

# 将分词、去停用词后的文本数据存储在list类型的texts中
texts = []
for line in documents:
    words = ' '.join(jieba.cut(line)).split(' ')  # 利用jieba工具进行中文分词
    text = []
    # 过滤停用词，只保留不属于停用词的词语
    for word in words:
        if word not in stopwords:
            text.append(word)
    texts.append(text)
for line in texts:
    print(line)

# 待比较的文档也进行预处理（同上）
words = ' '.join(jieba.cut(new_doc)).split(' ')
new_text = []
for word in words:
    if word not in stopwords:
        new_text.append(word)
print(new_text)

# 2.计算词频
print('2.计算词频')
frequency = defaultdict(int)  # 构建一个字典对象
# 遍历分词后的结果集，计算每个词出现的频率
for text in texts:
    for word in text:
        frequency[word] += 1
# 选择频率大于1的词(根据实际需求确定)
texts = [[word for word in text if frequency[word] > 1] for text in texts]
for line in texts:
    print(line)

# 3.创建字典（单词与编号之间的映射）
print('3.创建字典（单词与编号之间的映射）')
dictionary = corpora.Dictionary(texts)
print(dictionary)
# 打印字典，key为单词，value为单词的编号
print(dictionary.token2id)

# 4.将待比较的文档转换为向量（词袋表示方法）
print('4.将待比较的文档转换为向量（词袋表示方法）')
# 使用doc2bow方法对每个不同单词的词频进行了统计，并将单词转换为其编号，然后以稀疏向量的形式返回结果
new_vec = dictionary.doc2bow(new_text)
print(new_vec)

# 5.建立语料库
print('5.建立语料库')
# 将每一篇文档转换为向量
corpus = [dictionary.doc2bow(text) for text in texts]
print(corpus)

# 6.初始化模型
print('6.初始化模型')
# 初始化一个tfidf模型,可以用它来转换向量（词袋整数计数），表示方法为新的表示方法（Tfidf 实数权重）
tfidf = models.TfidfModel(corpus)
# 将整个语料库转为tfidf表示方法
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)

# 7.创建索引
print('7.创建索引')
# 使用上一步得到的带有tfidf值的语料库建立索引
index = similarities.MatrixSimilarity(corpus_tfidf)

# 8.相似度计算并返回相似度最大的文本
print('# 8.相似度计算并返回相似度最大的文本')
new_vec_tfidf = tfidf[new_vec]  # 将待比较文档转换为tfidf表示方法
print(new_vec_tfidf)
# 计算要比较的文档与语料库中每篇文档的相似度
sims = index[new_vec_tfidf]
print(sims)
sims_list = sims.tolist()
# print(sims_list.index(max(sims_list)))  # 返回最大值
print("最相似的文本为：", documents[sims_list.index(max(sims_list))])  # 返回相似度最大的文本
