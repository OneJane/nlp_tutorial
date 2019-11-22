# -*- coding: utf-8 -*-

import os
import nltk

dir = "../CRF_TEST"

sentence = "Venezuelan opposition leader and self-proclaimed interim president Juan Guaidó said Thursday he will return to his country by Monday, and that a dialogue with President Nicolas Maduro won't be possible without discussing elections."
#sentence = "Real Madrid's season on the brink after 3-0 Barcelona defeat"
# sentence = "British artist David Hockney is known as a voracious smoker, but the habit got him into a scrape in Amsterdam on Wednesday."
# sentence = "India is waiting for the release of an pilot who has been in Pakistani custody since he was shot down over Kashmir on Wednesday, a goodwill gesture which could defuse the gravest crisis in the disputed border region in years."
# sentence = "Instead, President Donald Trump's second meeting with North Korean despot Kim Jong Un ended in a most uncharacteristic fashion for a showman commander in chief: fizzle."
# sentence = "And in a press conference at the Civic Leadership Academy in Queens, de Blasio said the program is already working."
#sentence = "The United States is a founding member of the United Nations, World Bank, International Monetary Fund."

default_wt = nltk.word_tokenize # 分词
words = default_wt(sentence)
print(words)
postags = nltk.pos_tag(words)
print(postags)

with open("%s/NER_predict.data" % dir, 'w', encoding='utf-8') as f:
    for item in postags:
        f.write(item[0]+' '+item[1]+' O\n')

print("write successfully!")

os.chdir(dir)
os.system("crf_test -m model NER_predict.data > predict.txt")
print("get predict file!")

# 读取预测文件redict.txt
with open("%s/predict.txt" % dir, 'r', encoding='utf-8') as f:
    sents = [line.strip() for line in f.readlines() if line.strip()]

word = []
predict = []

for sent in sents:
    words = sent.split()
    word.append(words[0])
    predict.append(words[-1])

# print(word)
# print(predict)

# 去掉NER标注为O的元素
ner_reg_list = []
for word, tag in zip(word, predict):
    if tag != 'O':
        ner_reg_list.append((word, tag))

# 输出模型的NER识别结果
print("NER识别结果：")
if ner_reg_list:
    for i, item in enumerate(ner_reg_list):
        if item[1].startswith('B'):
            end = i+1
            while end <= len(ner_reg_list)-1 and ner_reg_list[end][1].startswith('I'):
                end += 1

            ner_type = item[1].split('-')[1]
            ner_type_dict = {'PER': 'PERSON: ',
                             'LOC': 'LOCATION: ',
                             'ORG': 'ORGANIZATION: ',
                             'MISC': 'MISC: '
                            }
            print(ner_type_dict[ner_type], ' '.join([item[0] for item in ner_reg_list[i:end]]))