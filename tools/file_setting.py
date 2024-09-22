class ExcelSetting():
    """重写：读取Excel配置"""
    @staticmethod
    def getExcelColToDict(sheet_name, colkey, colvalue, filepath='config/自动化配置.xlsx'):
        filepath = os.path.join(ROOT_PATH,filepath)
        file = pd.read_excel(filepath, sheet_name=sheet_name)
        dict_list = {}
        for k,v in zip(file[colkey], file[colvalue]):
            dict_list[k] = v
        return dict_list


