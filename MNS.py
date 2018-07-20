import pandas as pd
import numpy as np
import re

utfcsvfilepath = r'C:\Users\malihe.f\Desktop\malih\MNS.csv'
mainData = pd.read_csv(utfcsvfilepath, encoding = 'utf8')
del(mainData['Unnamed: 9'])
##mainData.head(3)

#clearing Data
mainData['sum_price2'] =  [x.strip().replace(',', '') for x in mainData.sum_price]
mainData['sum_price2'] =  [x.strip().replace('-', '0') for x in mainData.sum_price2]
mainData['sum_price2'] =  [x.strip().replace(')', '') for x in mainData.sum_price2]
mainData['sum_price2'] =  [x.strip().replace('(', '-') for x in mainData.sum_price2]
mainData['sum_price2'] = mainData.sum_price2.astype(float)#changing type

##mainData['sum_price'].describe()
    
DataTable = pd.pivot_table(mainData,
                           values=['sum_price2','cp_id'],
                           index=['cp_name','product_name_english'],
                           aggfunc= {'sum_price2':np.sum, 'cp_id':'count'})

for i in (DataTable.index.get_level_values('cp_name').unique()):
    result = DataTable.loc[i]
##    print(result)
    result.to_csv('C:\\Users\\malihe.f\\Desktop\\malih\\test\\{}.csv'.format(i),encoding='utf8')
##    result.to_csv(writer,'Sheet1')
##    writer.save()
