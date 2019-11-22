# 简介
Using Bi-LSTM model for NER in English.

语料库train.txt的前15行：每三行为一组，第一行为英语句子，第二行为每个句子的词性，第三行为NER系统的标注

```
played	on	Monday	(	home	team	in	CAPS	)	:
VBD	IN	NNP	(	NN	NN	IN	NNP	)	:
O	O	O	O	O	O	O	O	O	O
American	League
NNP	NNP
B-MISC	I-MISC
Cleveland	2	DETROIT	1
NNP	CD	NNP	CD
B-ORG	O	B-ORG	O
BALTIMORE	12	Oakland	11	(	10	innings	)
VB	CD	NNP	CD	(	CD	NN	)
B-ORG	O	B-ORG	O	O	O	O	O
TORONTO	5	Minnesota	3
TO	CD	NNP	CD
B-ORG	O	B-ORG	O
......
```
- utils.py: 项目配置及数据导入
- data_processing.py: 数据探索
- Bi_LSTM_Model_training.py: 模型创建及训练
- Bi_LSTM_Model_predict.py: 对新句子进行NER预测
 
## 项目配置 
utils.py文件中实现项目的配置及数据导入,设置了语料库文件的路径CORPUS_PATH，
KERAS模型保存路径KERAS_MODEL_SAVE_PATH，
在项目过程中会用到的三个字典的保存路径（以pickle文件形式保存）WORD_DICTIONARY_PATH，LABEL_DICTIONARY_PATH， OUTPUT_DICTIONARY_PATH。
load_data()函数，它将语料库中的文本以Pandas中的DataFrame结构展示出来

             word  pos     tag sent_no
    0      played  VBD       O       1
    1          on   IN       O       1
    2      Monday  NNP       O       1
> word这一列表示文本语料库中的单词，pos这一列表示该单词的词性，tag这一列表示NER的标注，sent_no这一列表示该单词在第几个句子中

## 数据探索
data_processing.py即对输入的数据（input_data）进行一些数据review，
在该语料库中，一共有13998个句子，比预期的42000/3=14000个句子少两个。一个有24339个单词，单词量还是蛮大的，
当然，这里对单词没有做任何处理，直接保留了语料库中的形式（后期可以继续优化）。
NER的标注列表为['O' ,'B-MISC', 'I-MISC', 'B-ORG' ,'I-ORG', 'B-PER' ,'B-LOC' ,'I-PER', 'I-LOC','sO']，
因此，本项目的NER一共分为四类：PER（人名），LOC（位置），ORG（组织）以及MISC，其中B表示开始，I表示中间，O表示单字词，不计入NER，sO表示特殊单字词。
数据处理函数data_processing()，它的功能主要是实现单词、标签字典，并保存为pickle文件形式，便于后续直接调用

## 建模
Bi_LSTM_Model_training.py建立Bi-LSTM模型来训练训练
先是通过input_data_for_model()函数来处理好进入模型的数据，其参数为input_shape，即填充句子时的长度。然后是创建Bi-LSTM模型create_Bi_LSTM()
最后，是在输入的数据上进行模型训练，将原始的数据分为训练集和测试集，占比为9:1，训练的周期为10次。

## 模型训练
运行上述模型训练代码，一共训练10个周期，训练时间大概为500s，在训练集上的准确率达99%以上，在测试集上的平均准确率为95%以上

## 模型预测
预测新数据的识别结果的完整Python代码（Bi_LSTM_Model_predict.py）,
修改Bi_LSTM_Model_predict中sent = 'James is a world famous actor, whose home is in London.'测试结果

注：https://docs.floydhub.com/guides/environments/ 查看keras和tensorflow版本对应 pip install keras==2.2.4 pydot
conda install GraphViz --channel conda-forge -y

 