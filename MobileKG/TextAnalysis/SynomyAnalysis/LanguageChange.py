import synonyms
from translate import Translator
trans=Translator(from_lang="chinese",to_lang="english")
print(trans.translate("下一步"))
print(synonyms.nearby("用户名"))
print(synonyms.nearby("密码"))
print(synonyms.nearby("购物车"))
print(synonyms.nearby("购物"))
print(synonyms.nearby("按钮"))
print(synonyms.nearby("协议"))
print(synonyms.nearby("继续"))
