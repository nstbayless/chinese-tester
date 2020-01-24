def convert_pinyin(pinyin):
  # converts pinyin to standardized form for comparison
  pinyin = pinyin    \
    .replace("0","") \
    .replace(" ","") \
    .strip()

  return pinyin.lower();

def pretty_pinyin(pinyin):
  pinyin = pinyin.replace("0","") \
    .replace("1",u'\u0304') \
    .replace("2",u'\u0301') \
    .replace("3",u'\u030C') \
    .replace("4",u'\u0300') \
    .replace("v",u'u\u0308') \
    .replace("V",u'U\u0308') \
    .replace("5","")
  return pinyin

# converts bāo -> ba1o
def numeric_pinyin(pinyin):
    pinyin = pinyin         \
        .replace("ā", "a1") \
        .replace("á", "a2") \
        .replace("ă", "a3") \
        .replace("à", "a4") \
        .replace("ē", "e1") \
        .replace("é", "e2") \
        .replace("ĕ", "e3") \
        .replace("è", "e4") \
        .replace("ī", "i1") \
        .replace("í", "i2") \
        .replace("ĭ", "i3") \
        .replace("ì", "i4") \
        .replace("ō", "o1") \
        .replace("ó", "o2") \
        .replace("ŏ", "o3") \
        .replace("ò", "o4") \
        .replace("ū", "u1") \
        .replace("ú", "u2") \
        .replace("ŭ", "u3") \
        .replace("ù", "u4") \
        .replace("ü", "v")  \
        .replace("ǖ", "v1") \
        .replace("ǘ", "v2") \
        .replace("ǚ", "v3") \
        .replace("ǜ", "v4")
    return pinyin
