import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import glob
import japanize_matplotlib
from sklearn.linear_model import LinearRegression
import scipy.stats as stats
import seaborn



target_dir = './'
csv_list = glob.glob(target_dir + '*.csv')
csv_list.sort()
#del csv_list[3:16] # for debug use, reduce list
#csv_files = len(csv_list)
print('csv_list content', csv_list)
print('csv_list[0]', csv_list[0])
print('csv_list:',len(csv_list))


header_df = pd.read_csv(csv_list[0], encoding='utf8')
print('header df:', header_df.head())

for i in range(1,len(csv_list)):
#read_df = pd.read_csv(csv_list[0],encoding='utf8',index_col='No' ''',  header=None ''')
    read_df = pd.read_csv(csv_list[i],encoding='utf8')
    print('csv read context [0]', read_df.head())
    header_df = pd.concat([header_df, read_df],ignore_index=True)

#outlier_2s(header_df['取引価格（㎡単価）'])
#print('concat df:',header_df.count())

header_df = header_df.sort_values('地区名')
header_df = header_df.dropna(how='any')   # drop if any NA in column
header_df = header_df[(np.abs(stats.zscore(header_df['坪単価'])) < 3)]  # include only the data width in 3sigma
header_df.to_csv('./analysis/final_concat_df_mansion_cp932.csv', encoding='cp932')
header_df.to_csv('./analysis/final_concat_df_mansion_utf8.csv', encoding='utf8')

#collect area list
area = list(header_df['地区名'].value_counts().keys())
# for debug area = ['京橋']
#print('area list :', area)

# Following for-loop used to create new building price graphs

for i in area:
    area_df = header_df[ (header_df['地区名']==i) & (header_df['取引時築年数']== 0)]
    counts = area_df['地区名'].count()
    print('area_df lines', len(area_df))
    print(area_df.head(100)) 
    if len(area_df) != 0 :         # empty Dataframe check
        plt.figure(figsize=(5, 5))
        #plt.plot(area_df['取引時築年数'], area_df['坪単価'], 'o', label = '取引点')
        plt.plot(area_df['取引年'], area_df['坪単価'],'o', label = '取引点')
        x = area_df[['取引年']]
        x_values = x.values  # Change format Series to array
        #for debug print('linear model x',x_values)
        #X = np.array(x).reshape(-1, 1)
        y = area_df[['坪単価']]
        y_values = y.values  # Change format Series to array
        #for debug print('linear model y', y_values)
        #y = np.array(y).reshape(-1, 1)
        model_lr = LinearRegression()  # linear regression
        model_lr.fit(x_values, y_values)             # linear regression
        plt.plot(x_values, model_lr.predict(x_values), linestyle="solid", label='回帰直線')
        plt.title(i + '　新築取引件数' +  str(counts) + '件' + '\n' + '係数' +str(model_lr.coef_.astype(int)) +'円/年')
        plt.yticks( np.arange(0, 6000000, 1000000))
        #plt.xticks(np.arange(0, 50, 5))
        plt.ylabel('坪単価　[百万円]')
        plt.xlabel('取引年　[年]')
        plt.grid(True)
        plt.legend()
        #plt.savefig('./save_fig/fig_new_built/' + i + '.png', format="png", dpi=300)
        plt.savefig('./save_fig/fig_new_built/' + i +'.png', format="png", dpi=300)
        plt.show()

# Following for-loop used to create old building price graphs
'''
for i in area:
    area_df = header_df[header_df['地区名']==i ]
    counts = area_df['地区名'].count()
    print('area_df lines', len(area_df))
    print(area_df.head(100))
    plt.figure(figsize=(5, 5))
    #plt.plot(area_df['取引時築年数'], area_df['坪単価'], 'o', label = '取引点')
    plt.plot(area_df['取引時築年数'], area_df['坪単価'],'o', label = '取引点')
    x = area_df[['取引時築年数']]
    x_values = x.values  # Change format Series to array
    #for debug print('linear model x',x_values)
    #X = np.array(x).reshape(-1, 1)
    y = area_df[['坪単価']] 
    y_values = y.values  # Change format Series to array
    #for debug print('linear model y', y_values)
    #y = np.array(y).reshape(-1, 1)
    model_lr = LinearRegression()  # linear regression
    model_lr.fit(x_values, y_values)             # linear regression
    plt.plot(x_values, model_lr.predict(x_values), linestyle="solid", label='回帰直線')
    plt.title(i + '　取引件数' +  str(counts) + '件' + '\n' + '係数' +str(model_lr.coef_.astype(int)) +'円/年')
    plt.yticks( np.arange(0, 6000000, 1000000))
    plt.xticks(np.arange(0, 50, 5))
    plt.ylabel('坪単価　[百万円]')
    plt.xlabel('取引時築年数　[年]')
    plt.grid(True)
    plt.legend()
    plt.savefig('./save_fig/fig_w_outliers/' + i + '.png', format="png", dpi=300)
    #plt.savefig('./save_fig/fig_wo_outliers/' + i +'.png', format="png", dpi=300)
    #plt.show()
'''

print(area_df.head(100))


'''
for i, x  in enumerate(csv_list) :
    read_df = pd.read_csv(x,encoding='utf8',index_col='No', header=None)
    print(read_df.header())
    header_df = pd.concat([header_df, read_df])
'''
print('concat DF:',header_df.head())