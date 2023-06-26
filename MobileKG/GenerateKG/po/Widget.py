class Widget:
    def __init__(self, id, name, english):
        self.id: int = id
        self.name: str = name
        self.english: str = english

    def get_str(self):
        return '{id:' + str(self.id) + ',name:"' + self.name + '",english:"' + self.english + '"}'

    def to_dic(self):
        result = {
            "id": str(self.id),
            "name": self.name,
            "english": self.english
        }
        return result

    def from_dic(self, dic):
        self.id = int(dic["id"])
        self.name = dic["name"]
        self.english = dic["english"]
