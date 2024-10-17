import os
import json
from jsonpath import jsonpath


CURRENT_PATH = os.path.dirname(__file__)
print(CURRENT_PATH)

with open(os.path.join(CURRENT_PATH,'../data/help.json'),mode='r',encoding='utf-8') as f:
    list_plugins = json.load(f)

list_name = jsonpath(list_plugins,'$..name')

print(list_plugins)
print(list_name)

control = 'B'
for item in list_plugins:
    if item["name"] == control:
        value = item["display"]
        item["display"] = (int(value) +1 ) % 2 # 1变0，0变1
print('xin:',list_plugins)

with open(os.path.join(CURRENT_PATH,'../data/help.json'),mode='w',encoding='utf-8') as f:
    f.write(json.dumps(list_plugins))