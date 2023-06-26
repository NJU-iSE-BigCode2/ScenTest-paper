from MobileKG.GenerateKG.po.Content import Content
import synonyms
from MobileKG.Neo4j.GraphSearch import GraphSearch
import math
import json
from MobileKG.Config.RunConfig import graph_type
import re


class MessageCompare:
    TotalSame = 1
    Similar = 2
    Different = 3
    SIM_TXT = json.loads(open('../Config/SimilarTXTConfig.json', 'r', encoding='utf-8').read())[graph_type]

    def __init__(self):
        self.similarity = 0.9
        self.same = 0.99

    def is_cnt_similar(self, cnt1: Content, cnt2: Content):
        if cnt1 is None or cnt2 is None:
            return MessageCompare.Different
        cnt_sim, eng_sim, opt_sim, wid_sim, lay_sim, ocr_sim = 0, 0, 0, 0, 0, 0
        if cnt1.name is not None and cnt2.name is not None:
            cnt_sim = MessageCompare.txt_sim(cnt1.name, cnt2.name)
        if cnt1.english is not None and cnt2.english is not None:
            eng_sim = MessageCompare.txt_sim(cnt1.english, cnt2.english)
        if cnt1.opt is not None and cnt2.opt is not None:
            opt_sim = MessageCompare.txt_sim(cnt1.opt.name, cnt2.opt.name)
        if cnt1.widget is not None and cnt2.widget is not None:
            wid_sim = MessageCompare.txt_sim(cnt1.widget.name, cnt2.widget.name)
        if cnt1.layout is not None and cnt2.layout is not None:
            lay_sim = 0
        if cnt1.ocr is not None and cnt2.ocr is not None:
            ocr_sim = MessageCompare.txt_sim(cnt1.ocr.name, cnt2.ocr.name)
        sim = cnt_sim * 0.8 + eng_sim * 0.07 + ocr_sim * 0.07 + opt_sim * 0.02 + wid_sim * 0.02 + lay_sim * 0.02;
        if sim >= self.same or cnt_sim >= self.same:
            return MessageCompare.TotalSame
        elif sim >= self.similarity:
            return MessageCompare.Similar
        else:
            return MessageCompare.Different

    def get_similar_cnts(self, cnt):
        cnts = GraphSearch.get_all_contents()
        same = None
        similar = []
        for c in cnts:
            sim = self.is_cnt_similar(c, cnt)
            if sim == MessageCompare.TotalSame:
                same = c
                break
            elif sim == MessageCompare.Similar:
                similar.append(c)
        return same, similar

    @classmethod
    def txt_sim(cls, txt1, txt2):
        def mean_sim(chars1, chars2):
            if chars1=='' or chars2=='':
                return 0
            return synonyms.compare(chars1, chars2)

        def char_sim(chars1, chars2):
            if len(chars1) == 0 or len(chars2) == 0:
                return 0
            count = 0
            for c in chars1:
                if c in chars2:
                    count = count + 1
            return count * 1.0 / len(chars1)
            return

        def config_sim(chars1, chars2):
            if str(chars1).__eq__(chars2):
                return 1.0

            rate = 0
            for config in MessageCompare.SIM_TXT:
                if chars1 in config['words'] and chars2 in config['words']:
                    rate = config['rate']
                    break
                main_char = None
                compare_char = None 
                if (chars1 in config['words']) or (mean_sim(chars1, config['words'][0]) >= 0.9):
                    main_char = chars1
                    compare_char = chars2
                elif (chars2 in config['words']) or (mean_sim(chars2, config['words'][0]) >= 0.9):
                    main_char = chars2
                    compare_char = chars1
                if main_char is None:
                    for relate in config['related']:
                        if chars1 in relate['words'] and chars2 in relate['words'] and relate['inner_rate'] > rate:
                            rate = relate['inner_rate']
                    for reg in config['format']:
                        if re.search(reg['reg'], chars1) is not None and re.search(reg['reg'], chars2) is not None and \
                                reg['inner_rate'] > rate:
                            rate = reg['inner_rate']
                else:
                    for relate in config['related']:
                        if compare_char in relate['words']:
                            return relate['outer_rate']
                    for reg in config['format']:
                        if re.search(reg['reg'], compare_char) is not None:
                            return reg['outer_rate']

            return rate

        con_sim = config_sim(txt1, txt2)
        mea_sim = mean_sim(txt1, txt2)
        cha_sim = (char_sim(txt1, txt2) + char_sim(txt2, txt1)) / 2.0
        if con_sim != 0:
            return con_sim
        elif math.isnan(mea_sim):
            return cha_sim
        else:
            return mea_sim * 0.9 + cha_sim * 0.1
