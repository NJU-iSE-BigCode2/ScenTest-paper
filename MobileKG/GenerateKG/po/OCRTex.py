class OCRTex:
    def __init__(self, id, name, similar):
        self.id: int = id
        self.name: str = name
        self.similar: list = similar

    def get_str(self):
        return '{id:' + str(self.id) + ',name:"' + self.name + '"}'

    def to_dic(self):
        result = {
            "id": str(self.id),
            "name": self.name,
            "similar": []
        }
        if self.similar is not None:
            for sim in self.similar:
                temp = {
                    "id": sim.id,
                    "name": sim.name
                }
                result["similar"].append(temp)
        return result

    def from_dic(self, dic):
        self.id = int(dic['id'])
        self.name = dic['name']
        self.similar = []
        for sim in dic['similar']:
            o = OCRTex(int(sim['id']), sim['name'], [])
            self.similar.append(o)
        return
