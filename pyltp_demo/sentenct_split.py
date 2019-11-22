# -*- coding: utf-8 -*-
# 分句
from pyltp import SentenceSplitter

# 分句
doc = '据韩联社12月28日反映，美国防部发言人杰夫·莫莱尔27日表示，美国防部长盖茨将于2011年1月14日访问韩国。' \
      '盖茨原计划从明年1月9日至14日陆续访问中国和日本，目前，他决定在行程中增加对韩国的访问。莫莱尔表示，' \
      '盖茨在访韩期间将会晤韩国国防部长官金宽镇，就朝鲜近日的行动交换意见，同时商讨加强韩美两军同盟关系等问题，' \
      '拟定共同应对朝鲜挑衅和核计划的方案。'
sents = SentenceSplitter.split(doc)  # 分句


for sent in sents:
    print(sent)