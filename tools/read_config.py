import json
import os

import yaml
import pandas as pd


os.environ["HOME_PATH"] = os.getcwd().split("GoodGoodStudy")[0]
ROOT_PATH = os.path.join(os.environ.get("HOME_PATH"),"GoodGoodStudy")
class YamlConifg():
    """读取Yaml配置"""
    def __init__(self, filepath='config/config.yaml'):
        filepath = os.path.join(ROOT_PATH,filepath)
        with open(filepath,'r',encoding='utf-8') as f:
            self.result = yaml.load(f.read(),Loader=yaml.FullLoader)

    def get_value(self, key):
        """获取yaml配置，用.按层次取值"""
        key_map = key.split('.')
        temp_res = self.result
        for k in key_map:
            if temp_res is None:
                print('配置取值键不存在对应值，请检查！')
            temp_res = temp_res.get(k)
        return temp_res

class ExcelSetting():
    """读取Excel配置"""
    @staticmethod
    def getExcelColToDict(sheet_name, colkey, colvalue, filepath='config/自动化配置.xlsx'):
        filepath = os.path.join(ROOT_PATH,filepath)
        file = pd.read_excel(filepath, sheet_name=sheet_name)
        dict_list = {}
        for k,v in zip(file[colkey], file[colvalue]):
            dict_list[k] = v
        return dict_list


def read_body_para(file):
    """读取json文件作为接口入参"""
    with open(file, 'r', encoding='gbk') as read_json:
        content = json.load(read_json)
    return content


