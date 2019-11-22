"""
词形还原（Lemmatization）是文本预处理中的重要部分，与词干提取（stemming）很相似
词形还原就是去掉单词的词缀，提取单词的主干部分，通常提取后的单词会是字典中的单词，不同于词干提取（stemming），提取后的单词不一定会出现在单词中。比如，单词“cars”词形还原后的单词为“car”，单词“ate”词形还原后的单词为“eat”
"""
# 使用WordNet为我们提供了稳健的词形还原的函数
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()
# lemmatize nouns
print(wnl.lemmatize('cars', 'n'))
print(wnl.lemmatize('men', 'n'))

# lemmatize verbs
print(wnl.lemmatize('running', 'v'))
print(wnl.lemmatize('ate', 'v'))

# lemmatize adjectives
print(wnl.lemmatize('saddest', 'a'))
print(wnl.lemmatize('fancier', 'a'))

# 获取单词的词性 使用Parts of speech（POS）技术实现
sentence = 'The brown fox is quick and he is jumping over the lazy dog'
import nltk

tokens = nltk.word_tokenize(sentence)
tagged_sent = nltk.pos_tag(tokens)
print(tagged_sent)

"""
对句子中的单词进行词形还原
"""
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


# 获取单词的词性
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


sentence = 'football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal.'
tokens = word_tokenize(sentence)  # 分词
tagged_sent = pos_tag(tokens)  # 获取单词词性

wnl = WordNetLemmatizer()
lemmas_sent = []
for tag in tagged_sent:
    wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
    lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))  # 词形还原

print(lemmas_sent)
