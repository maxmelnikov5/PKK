# -*- coding: utf-8 -*-
"""
Редактор Spyder

"""
#%%
import urllib.request
import json
import csv
import time


#%%### Блок с переменными ####
l = 0
q = []
un = []
ParcelLen = 20
CadDistrNum = "54:35"
CadQuNum
DistrQuerLim = "1000"
les_codes = [
        '145000000000',
        '145001000000',
        '145002000000',
        '145003000000']

##%%Блок с функциями
#Чтение набора участков в кадастровом квартале
def CadDistrQuery(distr, lim):
    jsn = urllib.request.urlopen("https://pkk5.rosreestr.ru/api/features/1?sqo="+ distr + "&sqot=3&limit=" + lim).read()
    parsed_string = json.loads(jsn)
    lplotlist = parsed_string['features']
    return lplotlist

## Словарь кадастровых участков по кадастровым кварталам
def CadDistrQuery(distr, lim):
    distrlist = []
    jsn = urllib.request.urlopen("https://pkk5.rosreestr.ru/api/features/2?sqo="+ distr + "&sqot=3&limit=" + lim).read()
    parsed_string = json.loads(jsn)
    quartdict = parsed_string['features']
    for quart in quartdict:
        distrlist.append(quart['attrs']['id'])
    lplotlist = {}
    for dist in distrlist:
        jsn2 = urllib.request.urlopen("https://pkk5.rosreestr.ru/api/features/1?sqo="+ dist + "&sqot=2&limit=" + lim).read()
        parsed_quart = json.loads(jsn2)
        lplotlist[dist] = parsed_quart['features']
    return lplotlist

###Получение списка параметров участка
def PlotQuery( plotid ):
        url = "https://pkk5.rosreestr.ru/api/features/1/" + plotid
        plotreq = urllib.request.urlopen(url).read()
        parsed_plot = json.loads(plotreq)
        a = parsed_plot['feature']['attrs']['cn']
        b = parsed_plot['feature']['attrs']['util_code']
        c = parsed_plot['feature']['attrs']['util_by_doc']
        e = parsed_plot['feature']['attrs']['area_value']
        f = parsed_plot['feature']['attrs']['cad_cost']
        g = parsed_plot['feature']['attrs']['fp']
        d = [a, b, c, e, f, g]
        return d  

#def slicer (counter, batch_size, list_):
#    if counter > 0:
#        y = (counter * batch_size)
#        x = max(0, y - batch_size)
#        sliced = list_[int(x) : int(y)]
#        sliced.append(sliced)
#        slicer (counter, batch_size, list_)
#    return sliced

#Делаем из списка набор списков с фиксированным количеством значений
def longSlicer (counter, batch_len, list_):
    un1 = []
    a1 = list(range(1, int(counter + 2)))
#    print(a1)
    for i in a1:
        y = (i * batch_len)
        x = max(y - batch_len, 0)
        sliced = list_[int(x) : int(y)]
        un1.append(sliced)
    return un1

#Делаем из списка словарь с фиксированным количеством значений
def dictSlicer (counter, batch_len, list_):
    un1 = {}
    a1 = list(range(1, int(counter + 2)))
#    print(a1)
    for i in a1:
        y = (i * batch_len)
        x = max(y - batch_len, 0)
        sliced = list_[int(x) : int(y)]
#        print(sliced)
        un1[i] = sliced
    return un1

###############################################
#%%Блок программы#############
    
#%%Запрашиваем список участков в кадастровом районе

if len(q) == int(DistrQuerLim):
    for lplot in CadDistrQuery(CadDistrNum, DistrQuerLim):
        q.append(lplot['attrs']['id'])
else:
            

#for lplot in CadDistrQuery(CadDistrNum, DistrQuerLim):
#    q.append(lplot['attrs']['id'])


print("Всего в списке ", len(q), " участков.")

#%%#Генерируем набор сублистов ИЛИ словарь
ql = longSlicer((len(q)/ParcelLen), ParcelLen, q)
#ql = dictSlicer((len(q)/ParcelLen), ParcelLen, q)

print("Будет сделано ", len(ql), " запросов")

#%%#Пишем всё в файл, вариант со списком


errlist = [] ##Переменная со списком сублистов, в которых ошибка
for lists in ql:
    l = l + 1 ## Считаем, в каком месте списка мы сейчас
    print(l)
    try:
        with open('caduch_list.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=',')
            wr.writerow(['cn','util_code','util_by_doc','area_value','cad_cost', 'formprop'])
            for i in lists:
                un.append(PlotQuery(i))
            wr.writerows(un)
            time.sleep(10)
    except: 
        print("Всё сомалось на шаге", l )
        errlist.append(l)

print("Закончилось. Ошибки в кусках ", errlist)
print("Импортировано ",len(un), " участков")



#for lists in ql:
#    l = l + 1
#    print(l)
#    try:
#        with open('caduch_list_1.csv', 'w', newline='') as myfile:
#            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=',')
#            wr.writerow(['cn','util_code','util_by_doc','area_value','cad_cost', 'formprop'])
#            for i in ql[lists]:
#                un.append(PlotQuery(i))
#            wr.writerows(un)
#            time.sleep(10)
#    except: 
#        print("Всё сомалось на шаге", l, "пробуем дальше" )
#
#print("Шеф, усё готово") 




#что мне надо? Посмотреть, сколько элементов уже прошли, если все - закончили
#Если не все - нужно взять следующий элемент, для каждого элемента запустить функцию,
#есди ошибка - запустить снова с того места, где остановились.


#if len(q) > DistrQuerLim:
#    print('Всего в квартале ', len(q), ' участков')
#else:
#    print('не все участки вошли в список, увеличьте лимит! Сейчас лимит - ', DistrQuerLim)

    
#def ListResult (pl_l):
#    if (len(pl_l) > 0):
#        i = pl_l.pop(0)
#        un.append(PlotQuery(i))
#        ListResult(pl_l)
#
#try:
#    ListResult(q)
#except:
#    print('Ошибка, ждём 10 секунд, в списке осталось участков', len(q))
#    time.sleep(10)
#    ListResult(q)
#    
#print(len(un), 'попало в окончательный список')
#
#with open('caduch_list.csv', 'w', newline='') as myfile:
#      wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=',')
#      wr.writerow(['cn','util_code','util_by_doc','area_value','cad_cost', 'formprop'])
#      wr.writerows(un)
#
#print('Файл записан, конец скрипта!')

##HTTPError: Request Time-out