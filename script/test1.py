import os
import openpyxl
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows

CUR_PATH = os.path.dirname(__file__)
print(CUR_PATH)

file_path = os.path.join(CUR_PATH, '../data/周报.xlsx')
file_path_out = os.path.join(CUR_PATH, '../data/周报1.xlsx')

df = pd.read_excel(file_path)
df_out = df.loc[~df['模块'].str.contains('模型管理|日志管理|报表项方案'),:].head()

print(df,'\n',df_out)

wb = openpyxl.Workbook()
ws = wb.active

for r in dataframe_to_rows(df_out, index=False, header=True):
    ws.append(r)

wb.save(file_path_out)