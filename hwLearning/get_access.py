import requests

from api.aw import DoubanPlaform, PostPlaform

@cached(cache=TTLCache(maxsize=500,ttl=3 * 60))
def get_cookies(uid, passwd, cid):
    return get_cookies_realtime(uid, passwd, cid)

def get_cookies_realtime(uid, passwd, cid):
    data = {"uid": uid, "password": passwd, "fingerPrint": {"cid": cid}}
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    cookies = requests.post("https://passport.baidu.com/v2/getpublickey", data=data, headers=headers).cookies

    return cookies

def get_session(login_url, uid, passwd, cid, header_type, baseconfig):
    return get_session_realtime(login_url, uid, passwd, cid, header_type, baseconfig)

def get_session_realtime(login_url, uid, passwd, cid, header_type, baseconfig):
    if not cid:
        raise Exception('请传入有效的cid！')

    if 'shujia' in header_type:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
    elif header_type == 'CodeHub':
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }


    data = {"uid": uid, "password": passwd, "fingerPrint": {"cid": cid}}

    # 新建Session对象
    session = requests.Session()
    session.headers = headers

    # 创建登录的Session信息
    res = session.post(login_url, json=data, verify=False)
    if 'shujia' in header_type:
        cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
        cookies_str = ';'.join([f'{name}={value}' for name, value in cookies_dict.items()])
        session.headers.update({"Cookie": cookies_str})
    if header_type == 'CodeHub':
        session.headers.update(baseconfig.get_yaml_info('{}.headers'.format(header_type)))

    return session


if __name__ == '__main__':
    login_url = 'http://www.baidu.com'
    name = 'hello'
    pwd = 'world'
    cid = 'Time is short, I use python.'
    env = 'debugMode_sit'
    baseconfig = {}

    # 演示用法
    post = PostPlaform()
    post.session = get_session(login_url, name, pwd, cid, '{}'.format(env), baseconfig)  # 写入实例构造方法

    douban = DoubanPlaform()
    douban.cookie = get_cookies(name, pwd, cid)  # 写入实例构造方法