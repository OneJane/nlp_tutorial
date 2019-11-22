# Load saved model
import kashgari

loaded_model = kashgari.utils.load_model('time_ner.h5')

while True:
    text = input('sentence: ')
    t = loaded_model.predict([[char for char in text]])
    print(t)
# 经过工作人员两天的反复验证、严密测算，记者昨天从上海中心大厦得到确认：被誉为上海中心大厦“定楼神器”的阻尼器，在8月10日出现自2016年正式启用以来的最大摆幅。
# 早上9点25分到达北京火车站，火车站在北京市区哦，地铁很方便到达酒店，我们定了王府井大街的锦江之星，409元一晚，有点小贵。下午去了天坛公园，傍晚去了天安门广场。