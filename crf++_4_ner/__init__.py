# CRF，英文全称为conditional random field, 中文名为条件随机场，是给定一组输入随机变量条件下另一组输出随机变量的条件概率分布模型，其特点是假设输出随机变量构成马尔可夫（Markov）随机场。
# 线性链条件随机场可以用于序列标注等问题，而 命名实体识别(NER)任务正好可通过序列标注方法解决。
# 这时，在条件概率模型P(Y|X)中，Y是输出变量，表示标记序列（或状态序列），X是输入变量，表示需要标注的观测序列。
# 学习时，利用训练数据 集通过极大似然估计或正则化的极大似然估计得到条件概率模型p(Y|X)；预测时，对于给定的输入序列x，求出条件概率p(y|x)最大的输出序列y0
# 在自然语言处理技术走向实用化的过程中占有重要地位。一般来说，命名实体识别的任务就是识别出待处理文本中三大类（实体类、时间类和数字类）、七小类（人名、机构名、地名、时间、日期、货币和百分比）命名实体。
# 早期：基于规则 基于字典
# 传统机器学习：HMM MEMM CRF
# 深度学习方法：RNN-CRF CNN-CRF
# 近期：注意力模型 迁移学习 半监督学习
# linux:
#   https://taku910.github.io/crfpp/#download 0.58版本
#   tar zxf CRF++-0.58.tar.gz -C /usr/local/
#   cd /usr/local/CRF++-0.58
#   ./configure
#   make
#   make install
#   vim /etc/ld.so.conf 添加include /usr/local/lib
#   /sbin/ldconfig -v
#   crf_learn -v
#   cd CRF++-0.58/python && python setup.py install 如果报错 ln -s /usr/local/lib/libcrfpp.so.* /usr/lib64/
# windows:
#   CRF++ 0.58
"""
训练 crf_learn  -f 3 -c 4.0 template train.data model -t
        -f, –freq=INT使用属性的出现次数不少于INT(默认为1)
        -m, –maxiter=INT设置INT为LBFGS的最大迭代次数 (默认10k)
        -c, –cost=FLOAT    设置FLOAT为代价参数，过大会过度拟合 (默认1.0)
        -e, –eta=FLOAT设置终止标准FLOAT(默认0.0001)
        -C, –convert将文本模式转为二进制模式
        -t, –textmodel为调试建立文本模型文件
        -a, –algorithm=(CRF|MIRA)    选择训练算法，默认为CRF-L2
        -p, –thread=INT线程数(默认1)，利用多个CPU减少训练时间
        -H, –shrinking-size=INT    设置INT为最适宜的跌代变量次数 (默认20)
        -v, –version显示版本号并退出
        -h, –help显示帮助并退出

输出
    iter：迭代次数。当迭代次数达到maxiter时，迭代终止
    terr：标记错误率
    serr：句子错误率
    obj：当前对象的值。当这个值收敛到一个确定值的时候，训练完成
    diff：与上一个对象值之间的相对差。当此值低于eta时，训练完成

预测 crf_test -m model NER_predict.data > predict.txt

train.txt:该语料库一共42000行，每三行为一组，其中，第一行为英语句子，第二行为句子中每个单词的词性，第三行为NER系统的标注，共分4个标注类别：PER（人名），LOC（位置），ORG（组织）以及MISC，其中B表示开始，I表示中间，O表示单字词，不计入NER，sO表示特殊单字词

preprocess.py  拆分语料为训练集和测试集，得到NER_train.data, 此为训练集数据，NER_test.data，此为测试集数据
crf_learn -c 3.0 template NER_train.data model -t  训练该数据，一共迭代了193次，运行时间为490.32秒，标记错误率为0.00004，句子错误率为0.00056
crf_test -m model NER_test.data > result.txt  测试集上对该模型的预测表现做评估预测
statistics.py 统计预测的准确率
"""
