
from api import API
from post_aw import PostAW
from tools.read_config import YamlConifg
from tools.file_setting import ExcelSetting



class PostPlaform(PostAW):
    """Post平台相关方法，括号中按页签继承不同的类，如PostAW，PostModule，PostScript，PostTask等等"""
    def __init__(self):
        self.yc = YamlConifg()
        self.es = ExcelSetting()
        self.host = self.yc.get_value('Post.host')
        self.cookie = self.yc.get_value('Post.Cookie')
        self.headers = self.yc.get_value('Post.headers')
        self.branch = self.yc.get_value('Post.branch')

class DoubanPlaform():
    """豆瓣平台相关方法，括号中按页签继承不同的类，或者类中直接创建接口方法"""
    def __init__(self):
        self.yc = YamlConifg()
        self.es = ExcelSetting()
        self.host = self.yc.get_value('Douban.host')
        self.cookie = self.yc.get_value('Douban.Cookie')
        self.headers = self.yc.get_value('Douban.headers')
        self.branch = self.yc.get_value('Douban.branch')

    def douban_search(self, keyword):
        """豆瓣搜索"""
        method = 'GET'
        uri = f'/rexxar/api/v2/search'
        body = {"q": keyword, "type": "", "loc_id":"", "start":0, "count":10, "sort":"relevance"}

        return API(self.host, method, self.headers, uri, body).send_request()

def get_item_by_key(item, key):
    list = []
    for i in item:
        listLine = i.get(key) # 用i.get(key)而不用i[key]，是因为 字典取空时可以返回None而不会报错
        list.append(listLine)
    return list

if __name__ == '__main__':
    testaw = DoubanPlaform()
    x = testaw.douban_search('乘风破浪3')
    print(x)