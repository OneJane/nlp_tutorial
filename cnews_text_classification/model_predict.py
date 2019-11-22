# -*- coding: utf-8 -*-
# time: 2019-08-14 00:21
# place: Pudong Shanghai

import kashgari

# 加载模型
loaded_model = kashgari.utils.load_model('text_classification_model')

text = '违法嫌疑人KUEHN MARJAN AGNES于2014年10月15号持号码为F3709954的瑞士护照和号码为05311260的居留许可从浦东口岸入境。经查，该人于2014年01月05号从原住宿地点苏州市姑苏区公园天下13幢602室搬至苏州工业园区金湖湾花园9幢1902室并于当天入住。按照规定，KUEHN MARJAN AGNES应于入住园区金湖湾花园9幢1902室后二十四小时内向居住地派出所办理临时住宿登记，但其直到2015年06月12日才至公安机关申报，违反外国人住宿登记规定。'

x = [[_ for _ in text]]

label = loaded_model.predict(x)
print('预测分类:%s' % label)
