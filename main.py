import datetime  # библиотека для работы с датой и временем
# import requests # библиотека для работы c отправкой файлов(исполузется для работы с http запросами)
import vk_api # использование методов вк
import urllib.request # исполузется для работы с http запросами
import random #
import json # библиотека для работы с json форматом
from vk_api.longpoll import VkLongPoll, VkEventType # для работы с сообщениями

def statusmale(status):
    b = str()
    if status == "в сети":
        b = "появился"
        return b
    else:
        b = "вышел"
        return b

def crossHasID(id): # функция отвечает за значения в словаре. Проверяет есть ли у меня такой же ID искомого пользователя в других списках в словаре
    for i in crossIDs.values():
        if id in i:
            return True
    return False
# 81d235d1c4a7bac87080be4b1f4794d2c021c9963c895a75122bf3219e3ec8deb037d2eff556c57ab94c9
urlStr = "https://api.vk.com/method/users.get?user_ids={i}&fields=online&access_token={t}&v=5.131" # шаблон для работы с get.uesrs
token = '81d235d1c4a7bac87080be4b1f4794d2c021c9963c895a75122bf3219e3ec8deb037d2eff556c57ab94c9' # токен для подключения к API
maxint = 2147483647 # это максимальное значение для int32(нужно для присваивания каждому сообщению определённого идентификатора)
vk_session = vk_api.VkApi(token=token) # создаётся область для работы уже с методоами API через токен
longpoll = VkLongPoll(vk_session) # с пощью неё бот получает сообщения
vk = vk_session.get_api() # создаём переменную, в которую закладываем сессию с работающим API

crossIDs = {} # СЛОВАРЬ КЛЮЧЕЙ И ЭЛЕМЕНТОВ(СОДЕРЖИТ В СЕБЕ ID ИЩУЩЕГО ЧЕЛОВЕКА И ИСКОМЫХ ЛЮДЕЙ)
aimsDict = {} # СЛОВАРЬ ИСКОМЫХ ЛЮДЕЙ


while True: # НАЧАЛО ЦИКЛА
    events = longpoll.check() # функция получает события, действия в боте
    for event in events: #цикл обработки событий
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text: # если событие является сообщением, то
            if event.from_user: #событие от пользователя, а не от группы или кого-нибудь другого
                userId = event.user_id # запоминаем ID того, кто ищет, чтобы добавить в словарь
                text = event.text # Текст пришедшего сообщения
                if text.lower() == '/start': # Приветсвие
                    msg = "Привествую, список команд, доступных для дальнеших дейсвтий, можно посмотреть написав /help"
                    vk.messages.send(user_id=userId, message=msg, random_id=random.randint(0, maxint))

                elif text == '/help': # на команду /help отправляет список функций
                    outputMsg = "Добавить пользователя в список отслеживания ID - /add id\nУдалить пользователя из списка отслеживаня - /del id\nПосмотреть статус каждого пользователя в списке отслеживания ID - /now \nЗакончить работу с ботом - /end\nПросмотр статуса конкретного пользователя- /now id\n Просмотр всех пользователей с ID в списке отслеживания-/allCheckID\nЗапрос отчёта по конкретному пользователю(h - часы, m - минуты) - /report ID h m  \n " # объявляем строковую переменную  outputMsg
                    vk.messages.send(user_id=userId, message=outputMsg, random_id=random.randint(0, maxint)) # отправляем сообщение выше
                elif text.split()[0] == "/add": # добавляет нового пользователя в список отслеживания ID
                    aimId = text.split()[1] # Берем элемент из разрезанного текста под номером 1
                    if aimId.isdigit(): # Проверка текста на цифры(тип данных)
                        msg = "ID добавлен в список отслеживания"
                        if userId in crossIDs: # если пользователь в словаре
                            if aimId not in crossIDs[userId]: # Если искомого пользователя нет в словаре crossIDs по ключу userId
                                crossIDs[userId].append(aimId)# Добавить цель в список
                            else:
                                msg = "ID уже находится в списке отслеживания"
                        else:
                            crossIDs[userId] = [aimId] # Добавляем искомого пользователя в словарь
                        if aimId not in aimsDict: # Если искомого пользователя нет в словаре с искомыми пользователями
                            aimsDict[aimId] = -1 # Создаётся пустая запись об этом пользователе, чтобы добавить его позже

                        vk.messages.send(user_id=userId, message=msg,random_id=random.randint(0, maxint)) # мини-сообщение о добавлении пользователя
                        print(aimsDict) #Проверка словаря
                        print(crossIDs) #Проверка словаря
                    else:
                        vk.messages.send(user_id=userId, message="ID должен содержать только цифры", random_id=random.randint(0, maxint)) # Защита от дурака
                elif text.split()[0] == "/del":# delete #Удаляем пользователя из списка отслеживания ID
                    if userId in crossIDs:
                        aimId = text.split()[1] # Присваиваем переменной aimID ID искомого человека
                        if aimId.isdigit(): #Проверяем ID на дурака
                            if userId in crossIDs and aimId in crossIDs[userId]: #Если ищущий и искомый находятся в своих словарях, то
                                crossIDs[userId].remove(aimId) #Удаляется запись о пользователе из первого словаря
                                if not crossHasID(aimId): #Удалить из искомого словаря, если за этим пользователем никто больше не следит(если в первом словаре за ним никто не следит)
                                    del aimsDict[aimId] #Удаляем из второго словаря(Из словаря искомых)
                                vk.messages.send(user_id=userId, message="ID удалён из списка отслеживания", random_id=random.randint(0, maxint)) # Сообщаем от удалении
                            else:
                                vk.messages.send(user_id=userId, message="Введён несуществующий в списке отслеживания ID", random_id=random.randint(0, maxint)) #Проверяем на ID
                            print(aimsDict)
                            print(crossIDs)
                        else:
                            vk.messages.send(user_id=userId, message="ID должен содержать только цифры", random_id=random.randint(0, maxint))# Защита от дурака
                    else:
                        vk.messages.send(user_id=userId, message="У вас нет отслеживаемых целей", random_id=random.randint(0, maxint))
 #               elif text.split()[0] == "/delall":# delete #Удаляем пользователя из списка отслеживания ID
  #                  if userId in crossIDs and aimId in crossIDs[userId]:
   #                    while   > 0:
    #                    crossIDs[userId].remove(aimId) #Удаляется запись о пользователе из первого словаря
   #                     del aimsDict[aimId] #Удаляем из второго словаря(Из словаря искомых)
  #                     if len(crossIDs) == 0:
        #                   vk.messages.send(user_id=userId, message="Объекты удалены из списк отслеживания",random_id=random.randint(0, maxint))

  #                  else:
                     #   vk.messages.send(user_id=userId, message="У вас нет отслеживаемых целей", random_id=random.randint(0, maxint))
   #                 print(aimsDict)
  #                  print(crossIDs)

                elif text == "/end":
                    if userId in crossIDs:
                        del crossIDs[userId]
                        vk.messages.send(user_id=userId, message="Вы закончили работу с ботом",
                                         random_id=random.randint(0, maxint))
                    else:
                        vk.messages.send(user_id=userId, message="У вас нет отслеживаемых целей",
                                         random_id=random.randint(0, maxint))
                elif text == "/nowlist": # Запрашиваем текущий статус отслеживаемых пользователей
                    if userId in crossIDs:
                        vk.messages.send(user_id=userId, message="Список отслеживаемых ID:", random_id=random.randint(0, maxint))
                        outputMsg = "" # Создаем пустю строку
                        for aimId in crossIDs[userId]: #для каждого ID текущего пользователя, который отправил запрос /now
                            outputMsg += "Пользователь {0} в данный момент {1}\n".format(aimsDict[aimId]['name'], aimsDict[aimId]["status"]) #Добавляем в строку статус пользователя
                            # .format позволяет добавить в {0} и {1} имя и статус искомого человека из словаря искомых пользователей
                        vk.messages.send(user_id=userId, message=outputMsg, random_id=random.randint(0, maxint)) # Отправляем сообщение
                    else:
                        vk.messages.send(user_id=userId, message="У вас нет отслеживаемых целей", random_id=random.randint(0, maxint))
                elif text.split()[0] == "/now": # Вывод статус отдельного искомого пользователя
                    if userId in crossIDs:
                        if text == "/now":
                            vk.messages.send(user_id=userId, message="Вы не ввели ID пользователя. Повторите попытку, введя команду /now и черзе пробел ID пользователя", random_id=random.randint(0, maxint))
                        else:
                            if text.split()[1].isdigit(): # Проверка на дурака
                                if text.split()[1] in aimsDict:
                                    outputMsg = "Пользователь {0} в данный момент {1}\n".format(aimsDict[text.split()[1]]['name'], aimsDict[text.split()[1]]["status"])
                                    vk.messages.send(user_id=userId, message=outputMsg, random_id=random.randint(0, maxint))
                                # .format позволяет добавить в {0} и {1} имя и статус искомого человека из словаря искомых пользователей
                                else:
                                    vk.messages.send(user_id=userId,message="Пользователя с таким ID не существует в списке отслеживания", random_id=random.randint(0, maxint))
                            else:
                                vk.messages.send(user_id=userId, message="ID должен содержать только цифры", random_id=random.randint(0, maxint)) #Проверка на дурака
                    else:
                        vk.messages.send(user_id=userId, message="У вас нет отслеживаемых целей", random_id=random.randint(0, maxint))

                elif text == "/allCheckID": # Запрашиваем все отслеживаемые ID
                    if userId in crossIDs:
                        outputMsg = ""
                        for aimId in crossIDs[userId]: # для каждого искомого пользователя в словаре crossIDs
                            outputMsg += aimsDict[aimId]['name'] + " ID: " + aimId + "\n" #Добавляем в строковую переменную имя и ID
                        vk.messages.send(user_id=userId, message=outputMsg, random_id=random.randint(0, maxint)) #Выводим строку
                    else:
                        vk.messages.send(user_id=userId, message="У вас нет отслеживаемых целей", random_id=random.randint(0, maxint))
                elif text.split()[0] == "/report": # Запрашиваем отчёт
                    if text.split()[1].isdigit(): #проверка на числа
                        if userId in crossIDs:
                            reportDict = aimsDict[text.split()[1]]['report'] # создаём переменную reportDict, в которой хранится список времени и статуса введенного в /report пользователя
                            prms = text.split() #Создаём переменную(список), в которую вкладываем разрезанную строку(используем для удобства)
                            if len(prms) > 2:
                                currTime = datetime.datetime.now() #Переменная с текущим временем
                                h = int(prms[2]) # Мы берем второй элемент переменной prms, преоборазуем тип данных в int, присваиваем все это дело переменной h
                                 #Создаём переменную минуты, которая потом будет равна либо введенным данным(минутам), либо равна 0, если пользователь не ввёл минуты
                                m = 0
                                if len(prms) == 4: #смотрим длину списка, если она равна 4, то пользователь ввёл минуты
                                    m = int(prms[3]) #Присваивыем минуты введенные пользвателем
                                limTime = currTime.replace(hour=currTime.hour - h, minute = currTime.minute - m, second=0, microsecond=0) #Создаем предел времени, до которого будет осуществляться мониторинг
                                #активности заданного пользователя
                                #CurrTime.replace - беру текущую дату, отнимаю от неё h и m, введенные пользователем и все это запихиваю в лимит
                                #Пример: текущее время 8:30, пользователь ввёл 1:15, отнимаем 8:30-1:15 = получаем нижний порог времени, с которого велась запись
                                outStr = "Отчёт по пользователю {0}: \n".format(aimsDict[text.split()[1]]['name']) #Создаём строковую переменную outStr
                                for time in reportDict: #Прогоняем time(индекс) по списку, содержащего в себе данные о времени и статусе пользователя при выходе/входе
                                    if time[0] > limTime: #Если время в списке,содержащего в себе данные о времени и статусе пользователя при выходе/входе, больше нижнего порога, то выполняем
                                        outStr += time[0].strftime("Дата: %d.%m.%Y время: %H:%M")+time[1]+"\n" #Заполняем строку выодную строку: добавляю time[0](время) к time[1](Время и статус), так как ходим по списку reportDict, имеющий вид
                                        #reportDict = [["Время входа/выхода из VK", "Имя и статус"], ["Время входа/выхода из VK 2", "Имя и статус 2"]] reportDict[0][0]
                                        #time = ["Время входа/выхода из VK", "Имя и статус"]
                                        #time[0] = "Время входа/выхода из VK "
                                        #time[1] = "Имя и статус"
                             #   file_name = 'report.txt'
                             #   with open(file_name, 'a+') as f:  # open file in append mode
                              #      f.write(outStr)
                                vk.messages.send(user_id=userId, message=outStr, random_id=random.randint(0, maxint)) #Выводим получившийся отчёт
                                # result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=event.object.message['peer_id'])['upload_url'], files={'file': open(file_name, 'rb')}).text)
                                # jsonAnswer = vk.docs.save(file=result['file'], title='title', tags=[])
                                # vk.messages.send(peer_id=event.object.message['peer_id'], random_id=0,attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}")
                            else:
                                vk.messages.send(user_id=userId, message="Введён неверный формат команды",random_id=random.randint(0, maxint))
                        else:
                            vk.messages.send(user_id=userId,message="Пользователя с таким ID не существует в списке отслеживания", random_id=random.randint(0, maxint))
                    else:
                        vk.messages.send(user_id=userId, message="ID должен содержать только цифры", random_id=random.randint(0, maxint)) #Проверка на дурака

                else:
                    vk.messages.send(user_id=userId, message="Неизвестная команда, введите /help или напишите '/start'", random_id=random.randint(0, maxint)) #Выдаёт всегда, кода не найдено соответсвие с каждым if

    # update status
    aimIdsStr = ','.join(str(i) for i in aimsDict) # Список с ID искомых пользователей превратили в строку aimIdsStr и разделили запятыми
    response = urllib.request.urlopen(urlStr.format(i=aimIdsStr, t=token)).read() #Создаём переменную response, в которую сохраняем ответ от http запроса в urlStr(самое начало) в формате строки
    # Ответ от http запроса в urlStr(самое начало) в формате строки
    #       {
    # "response":[{
    # "id":210700286,
    # "first_name":"Lindsey",
    # "last_name":"Stirling",
    # "bdate":"21.9.1986"
    # }]
    # }
    dictResponse = json.loads(response)['response'] #Переделываем строку чуть выше в список,в списке содержатся ответы, пример которых указан чуть выше
    #json.loads(response) достаёт из пришедшего запроса response все данные и формирует список.
    #БЫЛО: [response:[id1:[], id2:[]]]
    #СТАЛО: [id1:[], id2:[]]
    for resp in dictResponse: #Создали цикл, в котором гуляем по каждому элементу списка
        currId = str(resp['id']) #Создаём строковую переменную, в которую сохраняем ID текущего в списке пользователя
        if int(resp['online']) == 1: #Если статус равен единице, то
            currStat = "в сети" #Создаём переменную CurrStat и записываем туда строку онлайн
        else:
            currStat = "не в сети"# Если же нет, то создаём переменную CurrStat и записываем туда строку оффлайн
        isChanged = False #Содаётся перменная, хранящая информацию о смене статуса
        if aimsDict[currId] != -1: #Если ячейка в словаре искомых пользователей не пустая, то
            if aimsDict[currId]['status'] != currStat: #Если текущий статус не равен предыдущему, то
                isChanged = True #Статус изменился
                aimsDict[currId]['report'].append([datetime.datetime.now(), " - В это время пользователь {0} {2} {1}".format(aimsDict[currId]['name'], aimsDict[currId]['status'], statusmale(aimsDict[currId]['status']))])
                #Берем пользователя из искомого словаря с текущим ID и добавляем изменения в отчёт, то есть
                #datetime.datetime.now() - текущая дата
                #В пустое пространство через метод строки format добавляем в  {0} значение -  aimsDict[currId]['name']
                #В пустое пространство через метод строки format добавляем в  {1} значение -  aimsDict[currId]['status']
                #
            aimsDict[currId]['isChanged'] = isChanged #Запоминаем для текущего пользователя, что статус был изменён
            aimsDict[currId]['status'] = currStat #Запоминаем для текущего пользователя именно офлайн или онлайн, а не факт самого изменения
        else: #Если ячейка пустая, то заполняем ей шаблонными данными, заполнение происходит чуть выше по коду
            aimsDict[currId] = {'name': "{0} {1}".format(resp['first_name'], resp['last_name']),
                                'status': currStat,
                                'isChanged': isChanged,
                                'report': []}

    # send updated status
    for userId in crossIDs: #Для каждого ИЩУЩЕГО пользователя
        outputMsg = "" #Создаём пустую строку
        for aimId in crossIDs[userId]: #Гуляем по искомы пользователям в каждом ищущем пользователе
            if aimsDict[aimId]['isChanged']: #Если статус искомого пользователя был изменён, то
                outputMsg += "Пользователь {0} {2} {1}\n".format(aimsDict[aimId]['name'], aimsDict[aimId]["status"], statusmale(aimsDict[currId]['status'])) #То во выходную строку добавляется сообщение об этом

        if len(outputMsg) != 0: #Если сообщение не пустое, то отправить его пользователю
            vk.messages.send(user_id=userId, message=outputMsg, random_id=random.randint(0, maxint))
