#!C:\Server\bin\Python\Python39\python.exe
# -*- coding: cp1251 -*-
print ("Content-type: text/html\n\n")
print
print ("<html><head>")
print ("")
print ("</head><body>")
print ("Hello.")

import cgi  
import json
import datetime
import vk_api 
import requests
import hashlib

print("test1")

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def getCountryOK(vk):
  if vk == 228: #ямайка
    return "10415454380"
  elif vk == 1: #Россия
    return "10414533690"
  elif vk == 2: #Украина
    return "10424076448"


f = open("C:/login.txt", "r")
vk_session = vk_api.VkApi(f.readline(), f.readline(), captcha_handler=captcha_handler)
vk_session.auth()
vk = vk_session.get_api()

#Загрузка данных из формы и их форматирование
form = cgi.FieldStorage() 
print("test2")
name = form.getvalue("name")
surName = form.getvalue("surName")
bdate = form.getvalue("bdate")
try:
    ageFrom = form.getvalue("ageFrom")
    ageTo = form.getvalue("ageTo")
    job = form.getvalue("job")
except: 
    ageFrom = ""
    ageTo = ""
    job = ""
if form.getvalue("bdate") != None:
    byear = bdate[0:4]
    bmonth = bdate[5:7]
    bday = bdate[8:10]
else:
    bdate = None
    bday = None
    bmonth = None
    byear = None
print("test3")
sex = form.getvalue("user_sex")
country = form.getvalue("country")
if form.getvalue("city") and country:
    print("test4")
    city = vk.database.getCities(country_id = country, q= form.getvalue("city"))["items"][0]["id"]
else:
    city = None
#ВКонтакте
searchResults=vk.users.search(q = name + ' ' + surName,  birth_day = bday, birth_month = bmonth,  birth_year = byear, sex = sex,  country = country, city = city, age_from = ageFrom, age_To = ageTo, company = job, count = 100, fields='bdate, city, photo_200_orig, screen_name, is_closed')
print("test5")
returnResults = []
# print(int(searchResults['count']))

print("test6")
# print(len(searchResults['items']))

for i in range(len(searchResults['items'])):
    if searchResults['items'][i]['is_closed'] == False:
        g = []
        id = ''
        name = ''
        surname = ''
        bdate = ''
        href = ''
        photo = ''
        city = ''
        id = searchResults['items'][i]['id']    
        name = searchResults['items'][i]['first_name']    
        surname = searchResults['items'][i]['last_name'] 
        try:
            bdate = searchResults['items'][i]['bdate']
        except: 
            bdate = '' 
        href = 'https://vk.com/' + searchResults['items'][i]['screen_name']    
        try: 
            photo = searchResults['items'][i]['photo_200_orig']
        except: 
            photo = ''    
        try: 
            city = searchResults['items'][i]['city']['title']
        except: 
            city = ''    
        g = [name, surname, bdate, href, photo, city, id]
        # print(g)
        returnResults.append(g)
# print(returnResults[0][0])


f = open('res.txt', 'w', encoding = "utf-8")
for item in returnResults:
    f.write("%s;%s;%s;%s;%s;%s;%s\n" % (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
f.close

print("test7")


#Одноклассники 

accToken = 'access_token=tkn1wp2gC0422oPUo4bG62J9tVcqEcv4uc9LRSwdSlm4bTdmnNbA4jYKQBokNkAPuvtCH'
appKey = 'application_key=CBLFAQJGDIHBABABA'
appSec = '8825c8ac78ab7523c0376d438aea9ba1'

headers = {'Content-Type':'application/json','Cookie': 'bci=5950650924462897331; _statid=4d1a418c-731e-4c3e-bcdf-7791d79340a2; viewport=824; _userIds=""; _suserIds=""; TZ=6; _flashVersion=0; nbp=; msg_conf=2468555756792551; cudr=0; klos=0; LASTSRV=ok.ru; CDN=; AUTHCODE=Jay_C25y0dgJpfLEaZ16qPQxwXyrcQxCD0XSqsRewIT75xx-YSebhWuHjwQeSnnl0j3dlrekAhtTZ5ORmnagEQGW5XRO0ewWPV8Cve8Ui4-5hUvT6CDTpt5K_RPo8QFFp1EtmLNSwtk0UGE_3; JSESSIONID=aea0980ba373a5d38160db32767149118a35ce44f2e573f6.100a24b6; TZD=6.7430; TD=7430'}  

json = {
  "id": 72,
  "parameters": {
    "query": "",
    "filters": {
      "st.cmd": "searchResult",
      "st.mode": "Users",
      "st.query": "",
      "st.grmode": "Groups"
    },
    "chunk": {
      "firstIndex": 0,
      "offset": 0
    },
    "prefetch": False
  }
}

print("test8")
if sex == 1:
    sex = "f"
elif sex == 2:
    sex = "m"
else: sex = None

json["parameters"]["query"] = name + " " + surName
json["parameters"]["filters"]["st.query"] = name + " " + surName
if bday!=None or bmonth!=None or bday!=None:
  if bday!=None:
    json["parameters"]["filters"]["st.bthDay"] = str(bday)
  if bmonth!=None:
    json["parameters"]["filters"]["st.bthMonth"] = str(bmonth)
  if byear!=None:
    json["parameters"]["filters"]["st.bthYear"] = str(byear)
elif ageTo!=None or ageFrom!=None:
  if ageTo!=None:
    json["parameters"]["filters"]["st.tillAge"] = str(ageTo)
  if ageFrom!=None:
    json["parameters"]["filters"]["st.fromAge"] = str(ageFrom)
if country!=None:
  json["parameters"]["filters"]["st.country"] = str(getCountryOK(country))
if city!=None:
  json["parameters"]["filters"]["st.location"] = city

print("test9")

r = requests.post('https://ok.ru/web-api/v2/search/portal', json=json, headers=headers)
r=r.json()
print('r')

try:
  l = len(r['result']['users']['values']['results'])
except: l = 0

returnResults = []
if l != 0: 
  for i in range(l):
    print("test13")
    g = []
    id = ''
    name = ''
    surname = ''
    age = ''
    href = ''
    photo = ''
    location = ''
    href = 'https://ok.ru' + r['result']['users']['values']['results'][i]['user']['info']['shortLink']
    name = r['result']['users']['values']['results'][i]['user']['info']['firstName']
    surname = r['result']['users']['values']['results'][i]['user']['info']['lastName']
    id = r['result']['users']['values']['results'][i]['user']['info']['uid']
    sigToMd = appKey + 'fields=BIRTHDAY,pic_fullformat=jsonmethod=users.getInfouids=' + id + appSec
    hash_object = hashlib.md5(sigToMd.encode())
    urlOKgetInfo = 'https://api.ok.ru/fb.do?' + appKey + '&fields=BIRTHDAY%2Cpic_full&format=json&method=users.getInfo&uids=' + id + '&sig=' + hash_object.hexdigest() + '&' + accToken  
    searchUserOK = requests.post(urlOKgetInfo)
    sk = searchUserOK.json()
    bdate = sk[0]['birthday']
    print("test12")
    try:
      city = r['result']['users']['values']['results'][i]['user']['location']  
    except:
      city = ''
    try:
      # photo = 'https:' + r['result']['users']['values']['results'][i]['user']['imageUrl'] 
      photo = sk[0]['pic_full']
    except:
      photo = ''
    
    g = [name, surname, bdate, href, photo, city, id]
    print("test11")
    #print(g)
    returnResults.append(g)
  # print(returnResults)


  f = open('resOK.txt', 'w', encoding = "utf-8")
  for item in returnResults:
      f.write("%s;%s;%s;%s;%s;%s;%s\n" % (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
  f.close
else:
  f = open('resOK.txt', 'w', encoding = "utf-8")
  f.write(" ")
  f.close

print ("</body></html>")


