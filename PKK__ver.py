### Query to PKK for OKS

#%%modules

import urllib.request
import json
import csv
import time

#%% Functions

#Чтение набора участков в кадастровом квартале
def CadDistrQuery(distr, lim):
    jsn = urllib.request.urlopen("https://pkk5.rosreestr.ru/api/features/1?sqo="+ distr + "&sqot=3&limit=" + lim).read()
    parsed_string = json.loads(jsn)
    lplotlist = parsed_string['features']
    return lplotlist

#Поиск ОКС в границах квартала
def OksQuery(quart):
    jsn = urllib.request.urlopen("https://pkk5.rosreestr.ru/api/features/5?sqo="+ quart + "&sqot=2&").read()
    parsed_string = json.loads(jsn)
    lplotlist = parsed_string['features']
    return lplotlist

#%% Soft

test = OksQuery("23:40:413076")
print(test)


#%%
