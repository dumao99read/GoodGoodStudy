from api.api import API
from api.post_aw import PostAW
from tools.read_config import YamlConifg
from tools.file_setting import ExcelSetting

class PostPlaform(PostAW)
    """Post平台相关方法，括号中按页签继承不同的类，如PostAW，PostModule，PostScript，PostTask等等"""
    def __init__(self):
        self.yc = YamlConifg()
        self.es = ExcelSetting()
        self.host = self.yc.get_value('Post.host')
        self.cookie = self.yc.get_value('Post.Cookie')
        self.headers = self.yc.get_value('Post.headers')
        self.branch = self.yc.get_value('Post.branch')


def get_item_by_key(item, key):
    list = []
    for i in item:
        listLine = i.get(key) # 用i.get(key)而不用i[key]，是因为 字典取空时可以返回None而不会报错
        list.append(listLine)
    return list