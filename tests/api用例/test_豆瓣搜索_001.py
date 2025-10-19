from api.aw import DoubanPlaform


def test_doubanCase_001():
    # TODO: 导入有误待解决
    testaw = DoubanPlaform()
    res = testaw.douban_search('乘风破浪3')
    movie_info = res.get('target_name')
    assert '乘风破浪3' in movie_info