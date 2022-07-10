# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from jeraconv import jeraconv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import glob


# jeraconv is enable to convert Japanese era to Western era
j2w = jeraconv.J2W()


def era_j2w(df, default_year) : # df,default_year in exception
    conv_year_dict = {}          #  default era dictionary declaration
    for je_year  in df.value_counts().keys():  # iterable keys from Series
        try:
            we_year = j2w.convert(je_year)
        except:      # assign default value in exception
           we_year = default_year
        finally: #  assign value referring with key in dict{ }
            conv_year_dict[je_year] = int(we_year) #
    df  = df.map(conv_year_dict).copy()  # complete df referring dict key: value table
    return df

pd.set_option('mode.chained_assignment', 'raise')
def op_data(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'OpenData_Analytics, {name}')  # Press ⌘F8 to toggle the breakpoint.

#Collect Chuo_ku csv file list
target_dir = '/Users/minuano/PycharmProjects/OpenData/RealEstateTransaction/Chuo-ku'
csv_list = glob.glob(target_dir + '/*.csv')
csv_list.sort()
# del csv_list[2:16] for debug use, reduce list
print('csv_list:',len(csv_list))
#Extract year part  and covert to integer from collecting csv files
trade_year_list =[int (x[-9:-5]) for x in csv_list]
print(trade_year_list)


# Generate null frame with a frame reading
'''
df = pd.read_csv(csv_list[0], encoding='utf8',index_col='No')
df.drop(df.index[0:], inplace = True)
print('null frame column only:', df)
'''

# for loop until all cvs files read out, i=0,1,... x = 'csv_list[0]', 'csv_list[1]'...
for i, x  in enumerate(csv_list) :    # start for-loop
    df_org = pd.read_csv(x,encoding='utf8',index_col='No')
   #df = pd.concat([df,read_df])

# remove rows with NA in  column '建築年'
    df_org = df_org.dropna(subset=['建築年','面積（㎡）'])
# choose analysis items of columns by copy
    df_select = df_org[['種類', '地区名', '取引価格（総額）','坪単価',
                                      '面積（㎡）','取引価格（㎡単価）', '建築年' ]].copy()
    df_select['面積（㎡）'] = pd.to_numeric(df_select['面積（㎡）'],errors='coerce')
# following dtypes with casting to prevent from ufunc divided error
    df_select['取引価格（総額）'] = df_select['取引価格（総額）'].astype(float)
    df_select['坪単価'] = df_select['坪単価'].astype(float)
    df_select['面積（㎡）'] = df_select['面積（㎡）'].astype(float)
    df_select['取引価格（㎡単価）'] = df_select['取引価格（㎡単価）'].astype(float)
#print(df_select.dtypes)

# Extract only '種類'== '中古マンション等'
    df_mansion = df_select[df_select['種類'] == '中古マンション等'].copy()
#print(df_mansion.head())

#Add new 2 columns
    df_mansion['取引時築年数'] = df_mansion['建築年']
    df_mansion['西暦築年'] = df_mansion['建築年']
    df_mansion['取引年'] = df_mansion['建築年']
#print('df_mansion DF lines', df_mansion.count())

# Convert Japanese era to Western era
    #traded_year = int(1945) # as of the traded year

# 2022.04.17
# Convert Japanese era to Western era
    df_mansion['西暦築年'] = era_j2w(df_mansion["建築年"], 1900)
    print('西暦築年', df_mansion['西暦築年'].head(50))

#Calcurate following items by iterrows
    for idx, row in df_mansion.iterrows() :
        df_mansion.loc[idx, '取引価格（㎡単価）'] = (row['取引価格（総額）'] // row['面積（㎡）'])
        df_mansion.loc[idx, '坪単価'] = (row['取引価格（総額）'] // (row['面積（㎡）']/3.3))
        df_mansion.loc[idx, '取引時築年数'] =  int(trade_year_list[i]) - row['西暦築年']
        df_mansion.loc[idx, '取引年'] = int(trade_year_list[i])

# Cast to integer
    df_mansion['取引時築年数'] = df_mansion['取引時築年数'].astype(int)
    df_mansion['西暦築年'] = df_mansion['西暦築年'].astype(int)
    df_mansion.loc['取引年'] = df_mansion['取引年'].astype(int)

    #print(df_mansion['西暦築年'])
    #print(df_mansion.head())

    print('trade_year_list', trade_year_list[i])

    # drop illegal rows in ['取引時経過築年'] column
    indexNames = df_mansion[df_mansion['取引時築年数'] > 100].index
    df_mansion.drop(indexNames , inplace=True)

# Write CSV testing'
    df_mansion.to_csv(str(trade_year_list[i]) + '_df_mansion.csv',encoding='cp932', index=False)
    # end for-loop

# new_one = pd.read_csv('13102_20053_20054_chuo_collecte_item.csv',encoding='utf8',index_col='No')
#df_mansion = df_select[df_select['種類']=='中古マンション等']


    print(df_mansion.head())
#print(df_mansion.info())

# end of function
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    op_data('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
