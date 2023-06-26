import jieba.posseg
import re


def extract_keyword(text):
    pattern = re.compile("“(.*)”")
    match_res = pattern.findall(text)
    verb = ""
    objects = ""
    if len(match_res)>0:
        objects = match_res[0]
        sub_str = text.split("“")[0]
        sentence_seged = jieba.posseg.cut(sub_str.strip())
        for pair in sentence_seged:
            if pair.flag != 'm' and pair.flag != 'x':
                verb += pair.word
    else:
        sentence_seged = jieba.posseg.cut(text.strip())
        first_verb = False
        for pair in sentence_seged:
            if not first_verb and pair.flag == 'v':
                first_verb = True
                verb = pair.word
            else:
                if pair.flag != 'm' and pair.flag != 'x':
                    objects += pair.word
    return verb, objects
