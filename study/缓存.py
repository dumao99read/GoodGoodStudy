# -*- coding: UTF-8 -*-
import time
from diskcache import Cache

# 初始化缓存目录
cache = Cache('./my_cache_dir')

@cache.memoize(expire=3)  # 缓存3秒
# @cache.memoize(expire=3 * 60)  # 缓存3分钟
def get_str():
    print('ladygaga')  # 如果走缓存，就不会打印这行；如果调用函数就会打印
    return 'superMan'

if __name__ == '__main__':
    for i in range(10):
        time.sleep(2)
        print(f'{i}:', get_str())