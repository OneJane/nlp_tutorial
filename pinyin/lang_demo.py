# 繁简体转换及获取拼音
from langconv import *

# 转换繁体到简体
def cht_2_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line

line_cht= '''
台北市長柯文哲今在臉書開直播，先向網友報告自己3月16日至24日要出訪美國東部4城市，接著他無預警宣布，
2月23日要先出訪以色列，預計停留4至5天。雖他強調台北市、以色列已在資安方面有所交流，也可到當地城市交流、
參觀產業創新等內容，但柯也說「也是去看看一個小國在這麼惡劣環境，howtosurvive，他的祕訣是什麼？」這番話，
也被解讀，頗有更上層樓、直指總統大位的思維。
'''

line_cht = line_cht.replace('\n', '')
ret_chs = cht_2_chs(line_cht)
print(ret_chs)

# 转换简体到繁体
def chs_2_cht(sentence):
    sentence = Converter('zh-hant').convert(sentence)
    return sentence

line_chs = '忧郁的台湾乌龟'
line_cht = chs_2_cht(line_chs)
print(line_cht)



from xpinyin import Pinyin

p = Pinyin()

# 默认分隔符为-
print(p.get_pinyin("上海"))

# 显示声调
print(p.get_pinyin("上海", tone_marks='marks'))
print(p.get_pinyin("上海", tone_marks='numbers'))

# 去掉分隔符
print(p.get_pinyin("上海", ''))
# 设为分隔符为空格
print(p.get_pinyin("上海", ' '))

# 获取拼音首字母
print(p.get_initial("上"))
print(p.get_initials("上海"))
print(p.get_initials("上海", ''))
print(p.get_initials("上海", ' '))