import time


def intersect(rect_a, rect_b):
    a_x1, a_y1, a_x2, a_y2 = rect_a.get_coordinates()
    b_x1, b_y1, b_x2, b_y2 = rect_b.get_coordinates()
    dx = max(0, min(a_x2, b_x2) - max(a_x1, b_x1))
    dy = max(0, min(a_y2, b_y2) - max(a_y1, b_y1))
    S_i = dx * dy
    S_a = (a_x2 - a_x1) * (a_y2 - a_y1)
    S_b = (b_x2 - b_x1) * (b_y2 - b_y1)
    return S_i / S_a, S_i / S_b, S_i / (S_a + S_b - S_i)


def merge(boundings, ocr_res, threshold=.70):
    mods = []
    for rect_o in ocr_res:
        best_match = (None, 0, 0, 0)
        for rect_c in boundings:
            ratio_o, ratio_c, ratio = intersect(rect_o, rect_c)
            if ratio > best_match[3]:
                best_match = (rect_c, ratio_o, ratio_c, ratio)
        rect_c, _, ratio_c, _ = best_match
        if rect_c is not None:
            if ratio_c > threshold:
                mods.append(('replace', rect_c, rect_o))
                for rect_cc in boundings:
                    if rect_cc == rect_c:
                        continue
                    _, ratio_cc, _ = intersect(rect_o, rect_cc)
                    if ratio_cc > threshold:
                        mods.append(('delete', rect_cc))
            else:
                mods.append(('add', rect_o))
        else:
            mods.append(('add', rect_o))
    for mod in set(mods):
        if mod[0] == 'replace':
            boundings[boundings.index(mod[1])] = mod[2]
        elif mod[0] == 'add':
            boundings.append(mod[1])
        elif mod[0] == 'delete':
            boundings.remove(mod[1])
    return boundings


def run(boundings, ocr_res, threshold=.70):
    start = time.time()
    res = merge(boundings, ocr_res, threshold=.70)
    print('Complete component extraction in {:.2f} seconds'.format(time.time() - start))
    return res
