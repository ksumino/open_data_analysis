# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



import pandas as pd
import numpy as np
pd.set_option('mode.chained_assignment', 'raise')
def op_data(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'OpenData_Analytics, {name}')  # Press ⌘F8 to toggle the breakpoint.

chuo_area = pd.read_csv('13102_20053_20054.csv',encoding='cp932',index_col='No')
chuo_collect_item = chuo_area[['種類', '地区名', '取引価格（総額）','坪単価',
                                      '面積（㎡）','取引価格（㎡単価）', '建築年' ]].copy()
chuo_collect_item['面積（㎡）'] = pd.to_numeric(chuo_collect_item['面積（㎡）'],errors='coerce')
# following dtypes with casting to prevent from ufunc divided error
chuo_collect_item['取引価格（総額）'] = chuo_collect_item['取引価格（総額）'].astype(float)
chuo_collect_item['坪単価'] = chuo_collect_item['坪単価'].astype(float)
chuo_collect_item['面積（㎡）'] = chuo_collect_item['面積（㎡）'].astype(float)
chuo_collect_item['取引価格（㎡単価）'] = chuo_collect_item['取引価格（㎡単価）'].astype(float)
print(chuo_collect_item.dtypes)

# Extract '種類'== '中古マンション等'
chuo_area_mansion = chuo_collect_item[chuo_collect_item['種類'] == '中古マンション等']
# Extend a row named 平米単価 with value 0
chuo_area_mansion['平米単価'] = chuo_area_mansion.建築年
print(chuo_area_mansion.head())

for idx, row in chuo_area_mansion.iterrows() :
    chuo_area_mansion.loc[idx, '取引価格（㎡単価）'] = row['取引価格（総額）'] // row['面積（㎡）']
    chuo_area_mansion.loc[idx, '坪単価'] = row['取引価格（総額）'] // (row['面積（㎡）']/3.3)
print(chuo_area_mansion.head())




# Write CSV testing
# chuo_collect_item.to_csv('13102_20053_20054_chuo_collecte_item.csv')
# new_one = pd.read_csv('13102_20053_20054_chuo_collecte_item.csv',encoding='utf8',index_col='No')
#chuo_area_mansion = chuo_collect_item[chuo_collect_item['種類']=='中古マンション等']


#print(chuo_area_mansion)
#print(chuo_area_mansion.info())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    op_data('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
