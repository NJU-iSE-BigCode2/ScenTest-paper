class Component:
    def __init__(self, dic):
        self.category = dic['category']
        self.x1 = dic['x1']
        self.y1 = dic['y1']
        self.x2 = dic['x2']
        self.y2 = dic['y2']
        self.ocr = dic['ocr']
        self.operation = ''
        self.cnt = ''
        self.cnt_id=''
        self.state='M'

    def to_dic(self):
        return {
            'category': self.category,
            'ocr': self.ocr,
            'operation': self.operation,
            'cnt': self.cnt,
            'cnt_id':self.cnt_id,
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'state':self.state
        }
