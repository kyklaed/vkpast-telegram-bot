# -*- coding: utf-8 -*-

import config
import telebot
import vk
import time
import random
import multigroup
import re
import datetime



session={}
vkapi= {}

bot = telebot.TeleBot(config.token)

id_pass=[]          #хранит id юзеров
password_set = ["111","222","333"]
stop_set=["stop","стоп"]

user_login = {}
user_password = {}


id_group = {}
owner_id_n = {}
owner_id_str ={}
ow = {} # хранит id для выбора из списка id групп

check_data={} #флаг для работы c сохранением времени и даты
time_dic={} #сюда сохраняется дата в виде строки
time_list={}#тут храним время в юникс кодировке

str_link_photo1 = {} #хранение собранных ссылок на фото
string_photo = {} # хранение собранных ссылок на фото
lst_link_photo = {} #хранит id фото
list_url = {} #текст поста
photo = {} #хранит айдишники фоток
tags = """\n\n#Куплю #Продам #Обменяю #Барахолка"""
end_dic = {} #хранит ключи к основному словарю

newconf={} # состояние для создания нового конфига
city={} # храним название города , необходимо для работы с бд
bufferstate={}  # стейт для хранения ввода с клавиатуры что бы не допустить подадания повтора в бд
menubot={} # стейт для меню бота для переключения между настройками и режимами
tablelinks={} #содержит строку с названием таблицы для сохранения ссылок и времени поста

time_origin={}# для функции вычисления следующего часа
time_test={} #аналогично для фнкции вычисления врмении
time_replace={}#для сохраннеия рабочей инфы функции вычисления даты и времени
time_origin_half = {} #так же для вычисления 30 минут
time_origin_twoh = {} #для вычисления +2 часа
iduser={} # сюда id usera из vk ссылка на чей пост в данный момент рассматривается
list_param={} #для проверки параметров в основной функции по связи с апи
id_user_for_check_bkl={} #хранит id для проверки по блжээк листу
id_user_stat_check = {} #хранит ответ после провреки id если по базе по блеклисту
city_get={} #хранит город активированного конфига
time_originpost={}

#new func variable
dic_group={} #хранит  айди группы и айди постов
wallget={} # хранит в себе результат запроса к апи, в функции pars_post
wall_id={} #хранит составной id для запроса в vk_api_func
this_id_group={} #хранятся айди групп для рандомного выбора
count_group_to_random={} #счетчик для рандома, защищается от зацикливания функции когда кончатся группы для получения ссылок
s={} #хранит результат запроса к апи вк
a={}

@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(message.from_user.id, """Все комманды вводятся в чат!
Конфиг —  запись в бд с необходимыми настройками  для атворизации в ВК и работы по репосту  из групп.
Постинг — отправка поста в группу в ВК


1. new - создание нового конфига
2. addpost -  активация функции постинга в группу
3. showcity - показывает список введенных конфигов
4. showconfig - после ввода команды вас попросят ввести город, после этого вам будет показан конфиг выбранного города
5. useconfig - установка конфига, необходимо ввести название города. Без установленного конфига функция addpost работать не будет
6. showuseconfig - просмотр установленного конфига
7. stopaddpost - выход из режима добавления постов, вводится только в режиме addpost

new – описание:
1. ввод города - город является ключем к всему функционалу по работе с конфигом, вводите город лучше сокращением spb,msk,ekb итд

2. id вашей группы - вводите один айди состоящий только из цифр

3. id групп доноров - вводите сколько хотите групп из которых вы будете брать необходимый вам материал. Группы вводятся 
цифрами через запятую без пробела в одну строку в одном сообщении

4. login vk.com - вводите номер телефона или емейл от страницы с которой будете отправлять пост в группу, у этой страницы 
должны быть права админа или модератора в группу куда отправляется пост

5. password vk.com - пароль для ранее введенного логина

addpost – команда
введя команду addpost активируется режим что бы выйти из него введите stopaddpost

1. команда state - вводится сразу после активации режима addpost, она выдает первый пост a так же команда показывается текущий пост !!

2. команда '0'(ноль) - ноль вводится в чат если выданный вам пост не подходит, после ввода система генерирует и выдает вам новый пост

3. команда '1'(единица) - вводится если пост вас устраивает и вы хотите его разместить в группе. после ввода единицы вам 
необходимо ввести дату и время опубликования поста. Внимание ! формат ввода даты и времни 240320171300 -  первый две цифры (24) - число месяца,  
следующие 2 цифры (03) - номер месяца следующие 4 цифры (2017) - год , следующие 4 цифры (1300) - это время часы и минуты, 
учесть что если например 9 часов утра то это вводится вот так -  0900

stop - выход из сессии, работает в любом режиме, обнуление любых установленных настроек""")
#запись в бд поля город
def new_city(message):  # созадем таблицу если ее нет, вносим название города
    print("1")
    if newconf[message.chat.id]==0 : # держит состояния
        dbase = multigroup.Addconfig('userlink', message.chat.id)
        dbase.addtable()
        dbase.addcitygroup(message.text)
        dbase.udate_nametablelinks(message.text)  # добавления ключа для будущего создания новых таблиц для линков
        newconf[message.chat.id] = 1
        city[message.chat.id] = message.text #сохранили название города

#запись в бд айди группы ( моей куда идет постинг )
def new_mygroup(message): # сохраняем id гуппы ( тут ваша группа)
    print("2")
    if newconf[message.chat.id]==1:
        dbase = multigroup.Addconfig('userlink', message.chat.id)
        if message.text.isdigit():
            dbase.addmygroup(message.text,city[message.chat.id])
            newconf[message.chat.id]=2
            bufferstate[message.chat.id].append(message.text) # стейт для сохранения состояния , что бы в бд не уходил предыдущий ввод с клавиатуры
        else:
            bot.send_message(message.from_user.id, "You did not enter numbers")

#запись в бд групп откуда идет постинг( из них берут посты для выборки постов)
def new_wheregroup(message): # сохрняем id групп откуда берем нужные посты
    print("3")
    bufferstate[message.chat.id].clear()  # стейт, обнуляем его
    recheckid={}
    recheckid[message.chat.id]=re.findall(r'[-0-9,]+',message.text)
    if newconf[message.chat.id]==2:
        if recheckid[message.chat.id][0] == message.text:
            recheckid[message.chat.id] = None
            dbase= multigroup.Addconfig('userlink',message.chat.id)
            dbase.addwheregroup(message.text,city[message.chat.id])
            newconf[message.chat.id]=3
            bufferstate[message.chat.id].append(message.text)
        else:
            bot.send_message(message.from_user.id, "Your input does not match the pattern or contains something other than numbers")
            recheckid[message.chat.id] = None


#запись в бд логина от странице с которой идет постинг
def new_uservk(message):
    print("4")
    bufferstate[message.chat.id].clear()
    if newconf[message.chat.id]==3:
        dbase=multigroup.Addconfig('userlink',message.chat.id)
        dbase.addspamuser(message.text,city[message.chat.id])
        newconf[message.chat.id]=4
        bufferstate[message.chat.id].append(message.text)
# запись в бд пароля от страницы в вк
def new_passvk(message):
    print("5")
    bufferstate[message.chat.id].clear()
    if newconf[message.chat.id]==4:
        dbase=multigroup.Addconfig('userlink',message.chat.id)
        dbase.addspampassword(message.text,city[message.chat.id])
        newconf[message.chat.id]=5

def new_spamtext(message):
    print("6")
    bufferstate[message.chat.id].clear()
    if newconf[message.chat.id] == 5:
        dbase = multigroup.Addconfig('userlink', message.chat.id)
        dbase.addspamtext(message.text, city[message.chat.id])

# показывает какие города вы ввели в бд
#нужно сделать обработку ошибки
def show_city(message):
    dbase = multigroup.Getconfig('userlink', message.chat.id)
    for item in dbase.get_city_list():
        bot.send_message(message.from_user.id, item)
    menubot[message.chat.id] = 0

#просмотр конфига по введенному городу
@bot.message_handler(func=lambda message: message.chat.id in id_pass and menubot[message.chat.id]==4 )
def show_config(message):
    dbase = multigroup.Getconfig('userlink', message.chat.id)
    showcnf=dbase.get_config(message.text)
    try:
        for item in showcnf:
            bot.send_message(message.from_user.id,item)
    except Exception as err:
        print('show_cnf err = ',err)
        bot.send_message(message.from_user.id, "There in no such record")
    menubot[message.chat.id] = 0

#фнкция активации конфига
@bot.message_handler(func=lambda message: message.chat.id in id_pass and menubot[message.chat.id]==5 )
def use_config(message):
    dbase = multigroup.Getconfig('userlink', message.chat.id)
    showcnf = dbase.get_config(message.text)
    #print(showcnf)
    try:
        city_get[message.chat.id]=showcnf[5]
        user_login[message.chat.id].append(showcnf[2])
        user_password[message.chat.id].append(showcnf[3])
        tablelinks[message.chat.id]=showcnf[4]

        session[message.chat.id] = vk.AuthSession(config.my_app_id, user_login[message.chat.id],
                                                  user_password[message.chat.id], scope='wall, messages')
        vkapi[message.chat.id] = vk.API(session[message.chat.id], v="5.62")

        id_group[message.chat.id].append(int("-"+str(showcnf[0])))

        owner_id_str[message.chat.id].append(showcnf[1].split(','))
        #print(owner_id_str)
        for item in owner_id_str[message.chat.id][0]:
            owner_id_n[message.chat.id].append(int('-'+item))
        bot.send_message(message.from_user.id, "config installed")

    except Exception as error_api:
        print("use cnf err = ",error_api)
        bot.send_message(message.from_user.id, "such a configuration is not found")
    menubot[message.chat.id] = 0

@bot.message_handler(func=lambda message: message.chat.id in id_pass and menubot[message.chat.id]==6 )
def show_use_config(message): #показывает активированный конфиг
    if message.chat.id in user_login and user_login[message.chat.id]!=[]:
        bot.send_message(message.from_user.id, "city = {0}".format(city_get[message.chat.id]))
        bot.send_message(message.from_user.id, "login = {0}".format(user_login[message.chat.id]))
        bot.send_message(message.from_user.id, "password = {0}".format(user_password[message.chat.id]))
        bot.send_message(message.from_user.id, "group id = {0}".format(id_group[message.chat.id]))
        bot.send_message(message.from_user.id, "from group id = {0}".format(owner_id_str[message.chat.id][0]))
        menubot[message.chat.id] = 0
    else:
        bot.send_message(message.from_user.id, "config not installed")
        menubot[message.chat.id] = 0

# функция ввода и вызова фнкций для записи в бд
@bot.message_handler(func=lambda message: message.chat.id in id_pass and menubot[message.chat.id]==1)
def new_add(message):
    if  newconf[message.chat.id]==0 and message.text.lower() not in stop_set:
        new_city(message)
        bot.send_message(message.from_user.id, "the city saved in the database")
        bot.send_message(message.from_user.id, "enter the ID of your group")

    elif newconf[message.chat.id]==1 and message.text != city[message.chat.id] and message.text.lower() not in stop_set:
        new_mygroup(message)
        if newconf[message.chat.id]==2:
            bot.send_message(message.from_user.id, "ID your group saved to the database")
            bot.send_message(message.from_user.id,"enter the group where you want to take the posts")

    elif newconf[message.chat.id]==2 and message.text != bufferstate[message.chat.id] and message.text.lower() not in stop_set:
        new_wheregroup(message)
        if newconf[message.chat.id]==3:
            bot.send_message(message.from_user.id,"group donors saved")
            bot.send_message(message.from_user.id, "enter the username vk.com")

    elif newconf[message.chat.id]==3 and message.text != bufferstate[message.chat.id] and message.text.lower() not in stop_set:
        new_uservk(message)
        bot.send_message(message.from_user.id, "username saved")
        bot.send_message(message.from_user.id, "enter the password of your account vk.com")

    elif newconf[message.chat.id]==4 and message.text != bufferstate[message.chat.id] and message.text.lower() not in stop_set:
        new_passvk(message)
        bot.send_message(message.from_user.id, "password saved")
        bot.send_message(message.from_user.id, "enter the your spam text")

    elif newconf[message.chat.id]==5 and message.text != bufferstate[message.chat.id] and message.text.lower() not in stop_set:
        new_spamtext(message)
        newconf[message.chat.id] = 0
        city[message.chat.id] = ""
        menubot[message.chat.id] = 0
        if menubot[message.chat.id] == 0:
            bot.send_message(message.from_user.id, "spam text saved")
            bot.send_message(message.from_user.id, "your config saved")

    elif message.text.lower() in stop_set and newconf[message.chat.id] in (0,1,2,3,4):
        access_close(message)


#основное меню бота
@bot.message_handler(func=lambda message: message.chat.id in id_pass and message.text.lower() in
                                            ['new','addpost','showcity','showconfig','useconfig','showuseconfig','stopaddpost']
                                            or message.text.lower() in stop_set)
def menu_bot(message):
    if message.text == "new":
        menubot[message.chat.id] = 1
        bot.send_message(message.from_user.id,"enter the name of the city")

    elif message.text == "addpost" and message.chat.id in id_group.keys():
        if id_group[message.chat.id] == []:
            bot.send_message(message.from_user.id, "Config is not installed, to install use the command 'useconfig'")
        else:
            bot.send_message(message.from_user.id, "wait for loading the config")
            pars_post(message)
            random_id_group(message)
            bot.send_message(message.from_user.id, "config loaded, click the 'state' for a start")
            addpostmenu_keyboard_for_user(message)

            menubot[message.chat.id]=2

    elif message.text == "showcity":
        menubot[message.chat.id] = 3
        show_city(message)

    elif message.text == "showconfig":
        menubot[message.chat.id]=4
        bot.send_message(message.from_user.id, "enter the city to view the config")

    elif message.text == "useconfig":
        session[message.chat.id] = None
        vkapi[message.chat.id] = None
        user_login[message.chat.id] = []
        user_password[message.chat.id] = []
        id_group[message.chat.id] = []
        city_get[message.chat.id] = None
        owner_id_str[message.chat.id] = []
        owner_id_n[message.chat.id] = []

        menubot[message.chat.id] = 5
        bot.send_message(message.from_user.id, "enter the city for the installation config")

    elif message.text == "showuseconfig":
        menubot[message.chat.id]= 6
        show_use_config(message)

    elif message.text == "stopaddpost":
        stopadd_post(message)

    elif message.text.lower() in stop_set:
        access_close(message)


def stopadd_post(message):
    try:
        newconf[message.chat.id] = None
        city[message.chat.id] = ""
        menubot[message.chat.id] = 0
        list_param[message.chat.id] = None
        id_user_for_check_bkl[message.chat.id] = None
        city_get[message.chat.id] = None

        if message.chat.id in user_login.keys():
            user_login[message.chat.id].clear()
            user_password[message.chat.id].clear()
            id_group[message.chat.id].clear()
            owner_id_str[message.chat.id].clear()
            owner_id_n[message.chat.id].clear()
            tablelinks[message.chat.id] = None

        if message.chat.id in this_id_group and message.chat.id in dic_group:
            this_id_group[message.chat.id].clear()
            dic_group[message.chat.id].clear()

        menu_keyboard_for_user(message)
        bot.send_message(message.from_user.id, "you left repost mode")
    except Exception as err:
        print("stop error", err)
        bot.send_message(message.from_user.id, "stop error")

def menu_keyboard_for_user(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.InlineKeyboardButton(text="new")
    btn2 = telebot.types.InlineKeyboardButton(text="addpost")
    btn3 = telebot.types.InlineKeyboardButton(text="useconfig")
    btn4 = telebot.types.InlineKeyboardButton(text="showconfig")
    btn5 = telebot.types.InlineKeyboardButton(text="showcity")
    btn6 = telebot.types.InlineKeyboardButton(text="showuseconfig")
    btn7 = telebot.types.InlineKeyboardButton(text="stop")
    btn8 = telebot.types.InlineKeyboardButton(text="stopaddpost")
    keyboard.add(btn1, btn2, btn3)
    keyboard.add(btn4, btn5, btn6)
    keyboard.add(btn7,btn8)
    bot.send_message(message.from_user.id,"welcome to a bot for promoting groups",reply_markup=keyboard)

def addpostmenu_keyboard_for_user(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.InlineKeyboardButton(text="state")
    btn2 = telebot.types.InlineKeyboardButton(text="1")
    btn3 = telebot.types.InlineKeyboardButton(text="0")
    btn4 = telebot.types.InlineKeyboardButton(text="stopaddpost")
    btn5 = telebot.types.InlineKeyboardButton(text="stop")
    keyboard.add(btn2,btn3)
    keyboard.add(btn1,btn4)
    keyboard.add(btn5)
    bot.send_message(message.from_user.id, "keyboard actv", reply_markup=keyboard)

def time_keyboard(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.InlineKeyboardButton(text="{0}".format(datapost_generator_hour(message)))
    btn2 = telebot.types.InlineKeyboardButton(text="{0}".format(datapost_generator_half(message)))
    btn3 = telebot.types.InlineKeyboardButton(text="{0}".format(datapost_generator_twohours(message)))
    keyboard.add(btn1,btn2,btn3)
    bot.send_message(message.from_user.id, "activation datatime keyboard", reply_markup=keyboard)

def datapost_generator_hour(message): #генерация часа для передачи юзеру в кнопку
    try:
        time_origin[message.chat.id]=time_dic[message.chat.id][0]
        time_test[message.chat.id] = time_dic[message.chat.id][0][8:10]

        if time_test[message.chat.id] in ['00', '01', '02', '03', '04', '05', '06', '07', '08']:
            time_replace[message.chat.id] = time_origin[message.chat.id][9:10]
            return time_origin[message.chat.id][:8] + "0{0}00".format(str(int(time_replace[message.chat.id]) + 1))

        elif time_test[message.chat.id] in ['11', '12', '13', '14', '15', '16', '17', '18']:
            time_replace[message.chat.id] = time_origin[message.chat.id][9:10]
            return time_origin[message.chat.id][:8] + "1{0}00".format(str(int(time_replace[message.chat.id]) + 1))

        elif time_test[message.chat.id] in ['20', '21', '22']:
            time_replace[message.chat.id] = time_origin[message.chat.id][9:10]
            return time_origin[message.chat.id][:8] + "2{0}00".format(str(int(time_replace[message.chat.id]) + 1))

        elif time_test[message.chat.id] in ['09', '10', '19', '23']:
            if time_test[message.chat.id] == '09':
                return time_origin[message.chat.id][:8] + "{0}00".format(10)
            elif time_test[message.chat.id] == '10':
                return time_origin[message.chat.id][:8] + "{0}00".format(11)
            elif time_test[message.chat.id] == '19':
                return time_origin[message.chat.id][:8] + "{0}00".format(20)
            elif time_test[message.chat.id] == '23':
                return time_origin[message.chat.id][:8] + "{0}000".format(0)

    except Exception as err:
        print('data post gener err = ', err)
        return "None"

def datapost_generator_half(message):
    try:
        time_origin_half[message.chat.id] = time_dic[message.chat.id][0]
        return time_origin_half[message.chat.id][:10] + "30"
    except Exception as err:
        print('data post half err = ', err)
        return "None"

def datapost_generator_twohours(message):
    try:
        time_origin_twoh[message.chat.id]=time_dic[message.chat.id][0]

        if time_origin_twoh[message.chat.id][8:10] == '22':
            return time_origin_twoh[message.chat.id][:8] + "2355"
        elif time_origin_twoh[message.chat.id][8:10] in ['00', '01', '02', '03', '04', '05', '06', '07']:
            return time_origin_twoh[message.chat.id][:8] + "0{0}00".format(str(int(time_origin_twoh[message.chat.id][9:10]) + 2))
        elif time_origin_twoh[message.chat.id][8:10] in ['08', '09']:
            return time_origin_twoh[message.chat.id][:8] + "{0}00".format(str(int(time_origin_twoh[message.chat.id][9:10]) + 2))
        elif time_origin_twoh[message.chat.id][8:10] in ['10','11','12','13','14','15','16','17','18','19','20','21']:
            return time_origin_twoh[message.chat.id][:8] + "{0}00".format(str(int(time_origin_twoh[message.chat.id][8:10]) + 2))


    except Exception as err:
        print('data post two hour = ', err)
        return "None"



#функция авторизации
@bot.message_handler(
    func=lambda message: message.text in password_set and message.chat.id not in id_pass)  # авторизация по паролю:
def login_usr(message):
    newconf[message.chat.id]=0
    bufferstate[message.chat.id]=[]
    menubot[message.chat.id]=0

    iduser[message.chat.id]=[]
    list_param[message.chat.id]=None
    id_user_for_check_bkl[message.chat.id]=None
    id_user_stat_check[message.chat.id]=0
    check_data[message.chat.id] = 0

    bot.send_message(message.from_user.id, "The correct password!")
    menu_keyboard_for_user(message)

    if message.chat.id not in id_pass:  # если id нет в списке значит добавляем
        id_pass.append(message.chat.id)
        #print(id_pass)
        bot.send_message(message.from_user.id, "Your ID")
        bot.send_message(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "You are already in the database")

@bot.message_handler(func=lambda message: message.text not in password_set and message.chat.id not in id_pass)
def access_check(message):
    return bot.send_message(message.from_user.id, "Password error!")

#функция закрытия сессии
def access_close(message): # сессия закрывается полностью с удалением пароля авторизации
    try:
        id_pass.remove(message.chat.id)
        newconf[message.chat.id] = None
        city[message.chat.id] = ""
        menubot[message.chat.id] = 0
        list_param[message.chat.id] = None
        id_user_for_check_bkl[message.chat.id]=None
        city_get[message.chat.id]=None

        print("11 = ",user_login[message.chat.id], user_password[message.chat.id], id_group[message.chat.id],
              owner_id_str[message.chat.id], tablelinks[message.chat.id])

        if message.chat.id in user_login.keys():
            user_login[message.chat.id].clear()
            user_password[message.chat.id].clear()
            id_group[message.chat.id].clear()
            owner_id_str[message.chat.id].clear()
            owner_id_n[message.chat.id].clear()
            tablelinks[message.chat.id] = None
            print("22 = ",user_login[message.chat.id],user_password[message.chat.id],id_group[message.chat.id],
                  owner_id_str[message.chat.id],tablelinks[message.chat.id])

        if message.chat.id in this_id_group and message.chat.id in dic_group:
            this_id_group[message.chat.id].clear()
            dic_group[message.chat.id].clear()
        return bot.send_message(message.from_user.id, "session closed")
    except Exception as err:
        print("close err",err)
        bot.send_message(message.from_user.id, "you're still not authorized")

def pars_post(message):
    count_group_to_random[message.chat.id]=0
    this_id_group[message.chat.id] = []
    dic_group[message.chat.id] = {}
    #print(dic_group)
    timed = datetime.datetime.now() - datetime.timedelta(days=3)  # настоящее время минус 3 часа
    stamp2 = timed.timestamp()
    for group in owner_id_str[message.chat.id][0]:
        print(group,type(group))
        dic_group[message.chat.id][group] = []
        time.sleep(0.5)
        try:
            wallget[message.chat.id] = vkapi[message.chat.id].wall.get(owner_id=int('-' + group), offset=1, count=100)
        except Exception as err:
            print(err)
            dic_group[message.chat.id].pop(group)
            print(dic_group)
        for checkgr in wallget[message.chat.id]['items']:
            if 'signer_id' in checkgr and 'attachments' in checkgr and 'photo' in checkgr['attachments'][0] \
                    and 'copy_history' not in checkgr and checkgr['date'] > int(stamp2) and 'link' not in checkgr\
                    and message.chat.id in dic_group.keys() and group in dic_group[message.chat.id]:
                dic_group[message.chat.id][group].append(checkgr['id'])


def random_id_group(message):

    for indx in dic_group[message.chat.id].keys():
        if dic_group[message.chat.id][indx] !=[]:
            this_id_group[message.chat.id].append(indx)
    ow[message.chat.id]=random.choice(this_id_group[message.chat.id])
    print("random = ",ow[message.chat.id])
    if dic_group[message.chat.id][ow[message.chat.id]] != []:
        wall_id[message.chat.id]="-{0}_{1}".format(ow[message.chat.id],dic_group[message.chat.id][ow[message.chat.id]][0])
        print("wall_id = ",wall_id[message.chat.id])
        return wall_id[message.chat.id]
    else:
        count_group_to_random[message.chat.id]+=1
        print("COUNTTTTTT = ",count_group_to_random[message.chat.id])
        print("YOOOOOOOOOO = ",len(dic_group[message.chat.id].keys()))
        if count_group_to_random[message.chat.id] != len(dic_group[message.chat.id].keys()):
            random_id_group(message)
        else:
            bot.send_message(message.from_user.id, "end")
            wall_id[message.chat.id]=None
            stopadd_post(message)


def api_vk_func(message):  # основная функция доступа к апи вк
    try:
        a[message.chat.id] = vkapi[message.chat.id].wall.getById(posts=wall_id[message.chat.id])
        s[message.chat.id] = 'https://vk.com/public{0}?w=wall{1}'.format(ow[message.chat.id], wall_id[message.chat.id])
        print(s)
        list_param[message.chat.id] = a[message.chat.id][0]
    except Exception as err:
        print(err)

    try:
        time.sleep(1)
        time_originpost[message.chat.id] = time.strftime('%Y-%m-%d %H:%M',
                                                         time.localtime(list_param[message.chat.id]['date']))
        id_user_for_check_bkl[message.chat.id]=a[message.chat.id][0]['signer_id'] #для проверки по блек листу
        print(a[message.chat.id][0]['signer_id'])
        print(" id check bl = ", id_user_for_check_bkl[message.chat.id])
        k = multigroup.Check_black_list("blacklist", "bklist")
        id_user_stat_check[message.chat.id] = k.blacklist(id_user_for_check_bkl[message.chat.id]) #проврека по базе id на чс
        print("stat check bl= ",id_user_stat_check[message.chat.id])
        if id_user_stat_check[message.chat.id] == None:
            print("vse OK")
            return a[message.chat.id], s[message.chat.id]
        else:
            #time.sleep(1)
            dic_group[message.chat.id][ow[message.chat.id]].pop(0) # удаляем нулевой элемент
            random_id_group(message)

            print("Ne OK")
            return api_vk_func(message)  # если не Ок то еще вызываем функцию
    except Exception as err:
        print(err)



# командой стейт получем первый пост а так же омжно проверить какой пост сейчас на очереди
@bot.message_handler(func=lambda message: message.chat.id in id_pass and menubot[message.chat.id] == 2 and
                                          message.text.lower() in ['state','stopaddpost'] or message.text == "0")
def state_post(message):
    if message.text == "state":
        print('------------------------------------------------------------------')
        print("command = state")
        print('------------------------------------------------------------------')
        s[message.chat.id] = api_vk_func(message)
        bot.send_message(message.from_user.id, s[message.chat.id][1])
        bot.send_message(message.from_user.id, time_originpost[message.chat.id])

    if message.text == "0" and message.text != "state":  # комманда "0" - отказ от постинга объявы и переход к следующему
        print('------------------------------------------------------------------')
        print('command = 0')
        print('------------------------------------------------------------------')
        dic_group[message.chat.id][ow[message.chat.id]].pop(0)  # удаляем нулевой элемент
        random_id_group(message)  # генерация нового id группы
        s[message.chat.id] = api_vk_func(message)
        if s[message.chat.id] != None:
            bot.send_message(message.from_user.id, s[message.chat.id][1])
            bot.send_message(message.from_user.id, time_originpost[message.chat.id])


@bot.message_handler(func=lambda message: message.chat.id in id_pass and menubot[message.chat.id] == 2 and
                                          message.text == "1" or message.text.lower() in ['stopaddpost'])  # формирование поста
def add_post(message):
    print('------------------------------------------------------------------')
    print("command = 1")
    print('------------------------------------------------------------------')
    s[message.chat.id] = api_vk_func(message)
    if s[message.chat.id] !=None:
        text = s[message.chat.id][0][0]['text']  # получение текста из поста
        text_osn = re.sub(r"@[-\w\s\(]+", "", text).replace(')\n','') # регулярка для удаления например @club123 (Мото)
        text_osn += """\n\nПродавец: @id{0}""".format(s[message.chat.id][0][0]['signer_id'])  # берем id автора поста
        text_osn += tags  # добавляем теги

        dbase = multigroup.Addlinks('postlink', tablelinks[message.chat.id])
        dbase.addtablelinks()
        #print(s[0]['items'][0]['signer_id'], s[1])
        iduser[message.chat.id].append(s[message.chat.id][0][0]['signer_id']) #записываем id userа поста в список
        dbase.insert_db(s[message.chat.id][0][0]['signer_id'], s[message.chat.id][1])

        list_url[message.chat.id] = {}
        list_url[message.chat.id][s[message.chat.id][1]] = text_osn  # текст поста
        len_photo = s[message.chat.id][0][0]['attachments']  # список с прикрепленными файлами

        lst_link_photo[message.chat.id] = {}
        photo[message.chat.id] = []  # хранит айдишники фоток
        for j in range(len(len_photo)):
            print('-------------------------------------------------------------------------------------')
            print("PHOTO ==== ", s[message.chat.id][0][0]['attachments'][j])
            print('-------------------------------------------------------------------------------------')
            photo[message.chat.id].append(str(s[message.chat.id][0][0]['attachments'][j]['photo']['id']))  # id прикрепленных фото
        lst_link_photo[message.chat.id][s[message.chat.id][1]] = photo[message.chat.id]  # список с айди фото
        str_link_photo1[message.chat.id] = []

        for n in range(len(lst_link_photo[message.chat.id][s[message.chat.id][1]])):
            str_link_photo1[message.chat.id].append(
                "photo-{0}_{1}".format(ow[message.chat.id],
                                       str(lst_link_photo[message.chat.id][s[message.chat.id][1]][n])))  # собираем ссылку из id группы и id фото

        print("photo tyt = ",str_link_photo1[message.chat.id])
        string_photo[message.chat.id] = {}  # создает вложенный словарь
        string_photo[message.chat.id][s[message.chat.id][1]] = ', '.join(
            str_link_photo1[message.chat.id])  # преобразуем из списка в строку с разделителем запятая
        str_link_photo1[message.chat.id].clear()  # чистим  список с ссылками
        photo[message.chat.id].clear()  # чистим список с айдишками

        end_dic[message.chat.id] = []  # словарь для ключей для основго словаря
        for i in list_url[message.chat.id].keys():  # берем ссылку как id к словарям
            end_dic[message.chat.id].append(
                i)  # добавляем в словарь, словарь для хранения ссылок как ключей для  отправки поста
        if message.chat.id in time_dic and time_dic[message.chat.id] != []:  # печатаем дату последней публикации если она была
            bot.send_message(message.from_user.id,
                             "date and time of the last post {0}".format(time_dic[message.chat.id][0]))

        if message.chat.id in time_dic and time_dic[message.chat.id] != []:
            time_keyboard(message)  # генерация новоой даты с числом!!

        bot.send_message(message.from_user.id, "Enter the data and time")
        time_dic[message.chat.id] = []  # сюда сохраняется дата в виде строки
        time_list[message.chat.id] = []  # тут храним время в юникс кодировке
        check_data[message.chat.id] = 1  # флаг для работы c сохранением времени и даты



@bot.message_handler(func=lambda message: message.chat.id in id_pass and check_data[message.chat.id] == 1
                                          and message.text != "1" or message.text != "0")  # поcтинг в группу
def check_data_add(message):
    print('------------------------------------------------------------------')
    print("check_data_add")
    print('------------------------------------------------------------------')
    # формируем дату для отложенного постинга
    if len(message.text) == 12 and int(message.text) and check_data[message.chat.id] == 1:
        time_dic[message.chat.id].append(message.text)
        addpostmenu_keyboard_for_user(message)
        # берем срез и ставим в нужной последовательности
        time_list[message.chat.id].append(
            int(time.mktime(time.strptime('{0}-{1}-{2} {3}:{4}:00'.format(time_dic[message.chat.id][0][4:8],
                                                                          time_dic[message.chat.id][0][2:4],
                                                                          time_dic[message.chat.id][0][0:2],
                                                                          time_dic[message.chat.id][0][8:10],
                                                                          time_dic[message.chat.id][0][10:12]),

                                          '%Y-%m-%d %H:%M:%S'))))
        
        try:
            print('------------------------------------------------------------------')
            print('check data add:  try')
            print('time_dic = ',time_dic[message.chat.id])
            print('time_list = ',time_list[message.chat.id])
            print('------------------------------------------------------------------')
            vkapi[message.chat.id].wall.post(owner_id=id_group[message.chat.id][0], from_group=1,
                            message=list_url[message.chat.id][end_dic[message.chat.id][0]],
                            attachments=string_photo[message.chat.id][end_dic[message.chat.id][0]],
                            publish_date=time_list[message.chat.id][0])


            dbase = multigroup.Addlinks('postlink', tablelinks[message.chat.id])
            idmax = dbase.select_maxid()  # добавляем дату к последней записи ( провека по макисмальному айди в бд)
            link_to_post = link_post_my_group(message, time_list)
            dbase.update_maxid(time_list[message.chat.id][0], link_to_post, idmax)

            end_dic[message.chat.id].clear()  # чистим
            list_url[message.chat.id].clear()  # чистим
            time_list[message.chat.id].clear()
            bot.send_message(message.from_user.id, "Saved")

            dic_group[message.chat.id][ow[message.chat.id]].pop(0)  # удаляем нулевой элемент
            random_id_group(message)  # выбираем новую группу для взятия постов
            s[message.chat.id] = api_vk_func(message)
            bot.send_message(message.from_user.id, s[message.chat.id][1])
            bot.send_message(message.from_user.id, time_originpost[message.chat.id])
            iduser[message.chat.id].clear()
            check_data[message.chat.id] = 0


        except Exception as err:
            print('------------------------------------------------------------------')
            print('check data add: NOT try')
            print('time_dic = ', time_dic[message.chat.id])
            print('time_list = ', time_list[message.chat.id])
            print('------------------------------------------------------------------')
            print("check data err = ",err)
            print('------------------------------------------------------------------')
            end_dic[message.chat.id].clear()  # чистим
            list_url[message.chat.id].clear()  # чистим
            time_list[message.chat.id].clear()
            check_data[message.chat.id] = 0 # обнуляем стейт
            #удаляем из бд ранее занесенную запись если дата не верна
            if iduser[message.chat.id] != [] and menubot[message.chat.id] != 0:
                dbase = multigroup.Addlinks('postlink', tablelinks[message.chat.id])
                dbase.delete_null(iduser[message.chat.id][0])
                iduser[message.chat.id].clear()
            if menubot[message.chat.id] != 0:
                bot.send_message(message.from_user.id, "invalid publish date")
                bot.send_message(message.from_user.id,"Pleas press 1 or 0 , state")

    if len(message.text) != 12 and check_data[message.chat.id] == 1:
        addpostmenu_keyboard_for_user(message)
        bot.send_message(message.from_user.id, "Wrong format of date and time!")
        #bot.send_message(message.from_user.id, "Pleas press 1 or 0 , state")
        check_data[message.chat.id] = 0 # обнуляем стейт
        end_dic[message.chat.id].clear()  # чистим
        list_url[message.chat.id].clear()  # чистим
        time_list[message.chat.id].clear()
        # удаляем из бд ранее занесенную запись если дата не верна
        if iduser[message.chat.id] !=[]:
            dbase = multigroup.Addlinks('postlink', tablelinks[message.chat.id])
            dbase.delete_null(iduser[message.chat.id][0])
            iduser[message.chat.id].clear()

    if check_data[message.chat.id] == 0 and menubot[message.chat.id]==2:
        bot.send_message(message.from_user.id, "Pleas press 1 or 0 , state")


def link_post_my_group(message, time_list):  # ссылки на посты из моей группы для записи в базу
    a[message.chat.id] = vkapi[message.chat.id].wall.get(owner_id=id_group[message.chat.id][0], filter='postponed', offset=0,
                                        count=100)  # берем все возможные отложенне записи со стены
    for i in range(len(a[message.chat.id]['items'])):  # берем колличествов записей
        if a[message.chat.id]['items'][i]['date'] == time_list[message.chat.id][0]:  # беретдату и сравн. с последней введенной записью
            id_group_str = str(id_group[message.chat.id][0])  # ссылка на группу без минуса перед номером

            s = 'https://vk.com/public{0}?w=wall-{0}_{1}'.format(id_group_str[1:],  # id_group_str[2:-1],
                                                                 a[message.chat.id]['items'][i]['id'])  # формируем ссылку на пост
            return s

bot.polling(none_stop=True)
