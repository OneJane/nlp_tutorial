"""
利用词袋模型计算句子间余弦相似度
"""
sent1 = "I love sky, I love sea."
sent2 = "I like running, I love reading."

# 对于英语句子，可以使用NLTK中的word_tokenize函数生成两个list计算词频，对于中文句子，则可使用jieba模块进行分词
from nltk import word_tokenize

sents = [sent1, sent2]
texts = [[word for word in word_tokenize(sent)] for sent in sents]

# 分词完毕。下一步是构建语料库，即所有句子中出现的单词及标点并去重
all_list = []
for text in texts:
    all_list += text
corpus = set(all_list)
print(corpus)  # {'love', 'sea', 'sky', '.', 'like', 'reading', 'I', 'running', ','}

# 对语料库中的单词及标点建立数字映射，便于后续的句子的向量表示,将可迭代的corpus到爆成一个个元祖，返回有元祖组成的列表
corpus_dict = dict(zip(corpus, range(len(corpus))))
print(corpus_dict)  # {'love': 0, 'sea': 1, 'sky': 2, '.': 3, 'like': 4, 'reading': 5, 'I': 6, 'running': 7, ',': 8}


# 建立句子的向量表示，向量并不是简单地以单词或标点出现与否来选择0，1数字，而是把单词或标点的出现频数作为其对应的数字表示生成词袋模型
def vector_rep(text, corpus_dict):
    vec = []
    for key in corpus_dict.keys():
        if key in text:
            vec.append((corpus_dict[key], text.count(key)))
        else:
            vec.append((corpus_dict[key], 0))

    vec = sorted(vec, key=lambda x: x[0])

    return vec


vec1 = vector_rep(texts[0], corpus_dict)
vec2 = vector_rep(texts[1], corpus_dict)
print(vec1)  # [(0, 0), (1, 1), (2, 1), (3, 1), (4, 2), (5, 1), (6, 2), (7, 0), (8, 0)]
print(vec2)  # [(0, 1), (1, 0), (2, 1), (3, 1), (4, 2), (5, 0), (6, 1), (7, 1), (8, 1)]


# 利用词袋模型，即两个句子的向量表示，来计算相似度
from math import sqrt
def similarity_with_2_sents(vec1, vec2):
    inner_product = 0
    square_length_vec1 = 0
    square_length_vec2 = 0
    for tup1, tup2 in zip(vec1, vec2):
        inner_product += tup1[1]*tup2[1]
        square_length_vec1 += tup1[1]**2
        square_length_vec2 += tup2[1]**2

    return (inner_product/sqrt(square_length_vec1*square_length_vec2))

cosine_sim = similarity_with_2_sents(vec1, vec2)
print('两个句子的余弦相似度为： %.4f。'%cosine_sim)



"""
用gensim计算两个句子的相似度
"""
from gensim import corpora
from gensim.similarities import Similarity

#  语料库
dictionary = corpora.Dictionary(texts)

# 利用doc2bow作为词袋模型
corpus = [dictionary.doc2bow(text) for text in texts]
similarity = Similarity('-Similarity-index', corpus, num_features=len(dictionary))
print(similarity)
# 获取句子的相似度
new_sensence = sent1
test_corpus_1 = dictionary.doc2bow(word_tokenize(new_sensence))

cosine_sim = similarity[test_corpus_1][1]
print("利用gensim计算得到两个句子的相似度： %.4f。"%cosine_sim)
