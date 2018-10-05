import json
import urllib.request
token = '13b9626cc3dc9e1b5f11fe0799be0923770da2ff'

print('Важное примечание: программа разделена отступами, поэтому для продолжения работы Enter нужно будет нажимать 2 раза')
#функция, которая получает на вход список репозиториев 
def getting_users():
    users = []
    a = input('Введите имена пользователей гитхаба, с которыми будет произведена работа (когда закончите вводить, нажмите Enter 2 раза): ')
    while a != '':   
        users.append(a)
        a = input() #для того, чтобы закончить цикл 
    print('Список введеных репозиториев: ', users)
    return users
getting_users()


#функция ищет репозитории пользователя 
#задание1
#Выбрать какого-то одного пользователя из полученного списка и 
#распечатать список его репозиториев (name) и их описания (description). 
#Выбор пользователя должен осуществляться с помощью ввода с клавиатуры (функция input()).
def repositories(username, token):
    username = input('Выберите пользователя из данного списка: ')
    url = 'https://api.github.com/users/%s/repos?access_token=%s' % (username, token)  
    # по этой ссылке мы будем доставать джейсон, попробуйте вставить ссылку в браузер и посмотреть, что там
    response = urllib.request.urlopen(url)  # посылаем серверу запрос и достаем ответ
    text = response.read().decode('utf-8')  # читаем ответ в строку
    data = json.loads(text) # превращаем джейсон-строку в объекты питона

    print("1. Количество репозиториев у пользователя: ", len(data))  # сколько у пользователя репозиториев
    for i in data:
        print('Название репозитория и его описание: ')
        print('{}: "{}".'.format(i["name"], i["description"])) #названия и описания репозиториев  

repositories(input(), token) 


#задание2 
#Распечатать список языков (language) выбранного пользователя и количество репозиториев, в котором они используются
def languages(username,token):
    d = {}
    username = input('Повторно выберите пользователя для анализа языков в репозитории: ')
    url = 'https://api.github.com/users/%s/repos?access_token=%s' % (username, token)
    response = urllib.request.urlopen(url) 
    text = response.read().decode('utf-8') 
    data = json.loads(text) 
    for i in data:
        print('2. В репозитории ',i["name"],' используются следующие языки:', i["language"])
        if i['language'] in d:
            d[i['language']] +=1 
        else:
            d[i['language']] = 1 
    for i in d:
        print('Язык {} встречается в следующем количестве репозиториев: {}'.format(i,d[i]))
    return 

languages(input(), token) 

#задание3
#Узнать, у кого из пользователей в списке больше всего репозиториев.
def reps(users,token):
    leader = '' #имя пользователя гитхаба 
    number = 0 #число подписчиков 
    for user in users:
        url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user, token) 
        response = urllib.request.urlopen(url)  
        text = response.read().decode('utf-8')  
        data = json.loads(text)
        
        if len(data) > number:
            number = len(data)
            leader = user 
    print('3. Пользователь, у которого наибольшее количество репозиториев: ', leader)
    return 
users = getting_users()
reps(users, token)
        

    
    
#задание5
#Узнать, у кого из пользователей списка больше всего фолловеров?
def followers(users, token): 
    leader = '' #имя пользователя гитхаба
    number = 0  #число подписчиков
    for user in users:
        url = 'https://api.github.com/users/%s/followers?access_token=%s' % (user, token)  
        response = urllib.request.urlopen(url)  
        text = response.read().decode('utf-8')  
        data = json.loads(text)     

        if len(data) > number:
            number = len(data)
            leader = user
    print('4. Пользователь, у которого наибольшее количество подписчиков: ', leader)
    return 


users = getting_users()            
followers(users, token)
