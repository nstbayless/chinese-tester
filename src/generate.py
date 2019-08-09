# generate sentences

import random
import numpy as np
from math import floor

def xparams_agree(a, b):
    if a[0] == b[0]:
        if "any" in a[1]:
            return True
        if "any" in b[1]:
            return True
        for _a in a[1]:
            for _b in b[1]:
                if _a == _b:
                    return True
    return False

def xparam_rals_agree(ral_a, ral_b):
    for a in ral_a:
        for b in ral_b:
            if xparams_agree(a, b):
                return True
    return False

def parse_list_xparams(s):
    params = s.split(":")
    if len(params) == 0:
        raise "oops"
    return [params[0], params[1:], []]

#read as list
def ral(s):
    if isinstance(s, str):
        return list(map(
            lambda h: h.strip(),
            s.split(",")
        ))
    return s

def xparams_ral(s):
    pral = ral(s)
    o = [];
    for p in pral:
        o.append(parse_list_xparams(p))
    return o

def matches(v, type, hint=""):
    if type != "" and type != "any":
        v_type_ral = xparams_ral(v["type"])
        m_type_ral = xparams_ral(type)
        for xparams in m_type_ral:
            if len(xparams[1]) == 0:
                xparams[1].append("any")
        if not xparam_rals_agree(v_type_ral, m_type_ral):
            return False

    if hint != "" and hint != "any":
        v_hint_ral = xparams_ral(v["hint"])
        m_hint_ral = xparams_ral(hint)
        for xparams in m_hint_ral:
            if len(xparams[1]) == 0:
                xparams[1].append("any")
        if not xparam_rals_agree(v_hint_ral, m_hint_ral):
            return False

    return True

def word(vocab, type, hint=""):
    _np = list(filter(
        lambda v: matches(v, type, hint),
        vocab
    ))
    if len(_np) == 0:
        return {}, "&<t~" + type + "/h~" + hint + ">"
    w = np.random.choice(_np)
    return w, np.random.choice(w["character"])

def greetings(vocab):
    if np.random.random() < 0.2:
        return "你好"
    else:
        return word(vocab, "noun", "person")[1] + "你好"

def occupation(vocab):
    subj = word(vocab, "noun", "person")[1];
    occ = word(vocab, "noun", "occupation")[1]
    question = ""
    if np.random.random() < 0.1:
        question = "吗？";
    return subj + "是" + occ + question;

def punctuate_list(l):
    if len(l) == 0:
        return ""
    if len(l) == 1:
        return l[0]
    t = ""
    for w in range(0, len(l) - 2):
        t += l[w] + "、"
    return t + l[-2] + "和" + l[-1]

def digit(n, mark=""):
    if n == 0:
        return ""
    if n == 1:
        if mark != "":
            return mark
        return "一"
    if n == 2:
        return "二" + mark
    if n == 3:
        return "三" + mark
    if n == 4:
        return "四" + mark
    if n == 5:
        return "五" + mark
    if n == 6:
        return "六" + mark
    if n == 7:
        return "七" + mark
    if n == 8:
        return "八" + mark
    if n == 9:
        return "九" + mark
    return "&？<digit exceeds range>"

def number(n):
    s = ""
    if n == 0:
        if np.random.random() < 0.1:
            return "〇"
        return "零"
    bigdigit = 0
    bigdigitmark=["", "万", "亿", "兆", "京", "垓", "秭", "穰", "沟", "涧", "正", "载"]
    while n > 0:
        c = n % 10000
        us = ""
        if c > 0:
            ones = c % 10
            c = floor(c / 10)
            tens = c % 10
            c = floor(c / 10)
            hundreds = c % 10
            c = floor(c / 10)
            qians = c % 10
            us += digit(qians, "千")
            us += digit(hundreds, "百")
            us += digit(tens, "十")
            us += digit(ones)

        n = floor(n / 10000)
        s = us + bigdigitmark[bigdigit] + s
        bigdigit += 1
    return s


def number_of(counter, count):
    n = number(count)
    if n == "二":
        n = "两"
    return n + counter

def family_list(vocab):
    subj = word(vocab, "pronoun")[1]
    if np.random.random() < 0.1:
        subj = "家有几口人？"
    list = []
    if np.random.random() < 0.5:
        list.append(subj + "爸爸妈妈")
    else:
        if np.random.random() < 0.8:
            list.append(subj + "爸爸")
        if np.random.random() < 0.8:
            list.append(subj + "妈妈")
    used = ["爸爸", "妈妈"]
    while np.random.random() < 0.646:
        _word, family_member = word(vocab, "noun", "family-member");
        if family_member in used:
            continue
        used.append(family_member)
        if np.random.random() < 0.3 and not matches(_word, "noun", "single"):
            list.append(number_of("个", floor(0.999 + np.random.exponential(0.6))) + family_member)

    if len(list) == 0:
        return subj + "没有家"
    else:
        list.append(subj)
    return subj + "家有" + number_of("口", len(list)) + "人。 " + punctuate_list(list)


def normalize(weights):
    s = sum(weights)
    arr = []
    for w in weights:
        arr.append(w/s)
    return arr

def bignumber(vocab):
    c = np.random.random() * 10;
    k = np.random.random() * np.random.random() * 0.49 + 0.5
    while (np.random.random() < k) and c < 1000000000000000000000000000000000000.0:
        c *= 10
    c = floor(c)
    return number(c)

def specific_noun(vocab, hint):
    return word(vocab, "noun", hint)

def verb_get_hints_for_object(v, object):
    hints = v["hint"]
    if object in hints:
        return hints[object]
    return ""

def action(vocab):
    # sort of general-purpose way in which sentences are formed
    can_location = True
    s = ""
    wverb, verb = word(vocab, "verb")
    objects_opt = parse_list_xparams(wverb["type"])[1]
    if (len(objects_opt) == 0):
        objects = "s"
    else:
        objects = np.random.choice(objects_opt)
        if 's' not in objects:
            objects = "s" + objects
    #TODO: get from hint from verb's hint
    wsubj, subj = specific_noun(vocab, verb_get_hints_for_object(wverb, "s"))
    # TODO: decorate noun
    omit_subject = np.random.random() < .15
    if not omit_subject:
        s = subj

    # objects
    strobjects = []
    for object in objects:
        if object == "s":
            continue
        if object == "o" or object == "d":
            #TODO: get from hint from verb's hint
            noun = specific_noun(vocab, verb_get_hints_for_object(wverb, object))[1]
            strobjects.append(str(noun))
        if object == "l":
            strobjects.append("在" + word(vocab, "noun", "place")[1])
            can_location = False

    if can_location:
        # TODO
        pass

    s += verb
    for object in strobjects:
        s += object
    return s

def add_dot(s):
    if not s.endswith("？") and not s.endswith("。"):
        return s + "。"
    return s

def sentence(vocab):

    f = np.random.choice([
        greetings,
        occupation,
        family_list,
        bignumber,
        action
    ], p=normalize([0.24, 1, 1.5, 0.2, 50]))
    s = f(vocab)
    if f != bignumber:
        s = add_dot(s)
    return s
