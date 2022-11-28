### Query to PKK for OKS

#%%modules

import urllib.request
import json
import csv
import time
import pandas as pd

#%%
print('a')

#%% read info

testcn = '23:40:0:408'
url = 'http://rosreestr.ru/api/online/fir_object/'

jsn = urllib.request.urlopen(url + testcn).read()

#%%
parsed_string = json.loads(jsn)

#%% function
def OKSQuery(oksid):
    url = 'http://rosreestr.ru/api/online/fir_object/' #урл запроса
    jsn = urllib.request.urlopen(url + oksid).read() #get server responce
    parsed_string = json.loads(jsn) #parse json to dictionary
    #filter dictionary
    oksdict = {
    'ID': parsed_string['objectData']['id'],
    'objName' : parsed_string['objectData']['objectName'],
    'subtown' : parsed_string['objectData']['objectAddress']['locality'],
    'IDparc': parsed_string['parcelData']['id'],
    'area' : float(parsed_string['parcelData']['areaValue']),
    'areatype' : parsed_string['parcelData']['areaType'],
    'areaunit' : parsed_string['parcelData']['areaUnit'],
    'cost' : float(parsed_string['parcelData']['cadCost']),
    'buildtype' : parsed_string['parcelData']['oksType'],
    'year' : parsed_string['parcelData']['oksYearBuilt'],
    'floors' : parsed_string['parcelData']['oksFloors'],
    'isRemoved' : parsed_string['objectData']['removed']
    }
    return oksdict

#%% get list of cad numbes
cnlist = pd.read_csv('C:\OD\OneDrive\Documents\TempDocs\VSCode\PKK\Gel_cad.csv', sep=';')

#calllist = cnlist.CN_i.iloc[0:100].tolist() #filter list
calllist = cnlist.CN_i.tolist()

print('всего в списке '+str(len(calllist))+' объектов')

#%% get info for list

errlist = []
df3 = pd.DataFrame()
print('Query for ', len(calllist), 'objects')
n = 0
for i in calllist:
    try:
        n += 1
        df3 = df3.append(OKSQuery(i), ignore_index=True)
        print(n,' of ', len(calllist))
        time.sleep(2)
    except:
        print('Error on step ', n)
        errlist.append(i)
print('Done!')
print('Dataframe shape: ',df3.shape)
print('Errors count: ', len(errlist))
print('Writing output to gel.csv')
df3.to_csv('C:\OD\OneDrive\Documents\TempDocs\VSCode\PKK\gel.csv')


#%%tests
# df2 = pd.DataFrame.from_dict({iddd:sdict}, orient='index')

#df3.to_csv('testcsv.csv')

nn = 0
for i in [0, 1, 2, 3, 4]:
    #print(i)
    nn += 1
    print(nn)

#%%testcell

#testobj = OKSQuery('23:40:0:2050')

len(df3.objName.unique())

#%%
# parsed_string = json.loads(jsn)
#     quartdict = parsed_string['features']
#     for quart in quartdict:
#         distrlist.append(quart['attrs']['id'])
#     lplotlist = {}
#     for dist in distrlist:
#         jsn2 = urllib.request.urlopen("https://pkk5.rosreestr.ru/api/features/1?sqo="+ dist + "&sqot=2&limit=" + lim).read()
#         parsed_quart = json.loads(jsn2)
#         lplotlist[dist] = parsed_quart['features']
#     return lplotlist