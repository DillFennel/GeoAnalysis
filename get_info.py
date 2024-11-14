import json
import requests
import h3

#with open("data.json", encoding="UTF-8") as file_in:
#    data = json.load(file_in)

ya_geocode_api = '' #Для геокодера от Яндекса

ya_geocode_data = {} #Данные от Яндекс Геокодера
choosen_result = 0 #По умолчанию 0

def ya_geocode(address):#Адрес в  формате строки. Пример: "бул Мухаммед Бин Рашид, дом 1"
  global ya_geocode_data
  ya_geocode_data = requests.get('https://geocode-maps.yandex.ru/1.x/?apikey='+ya_geocode_api+'&geocode='+address.replace(' ', '+')+'&format=json').json()['response']['GeoObjectCollection']
def get_request(): #Выдает изначальный запрос
  return ya_geocode_data['metaDataProperty']['GeocoderResponseMetaData']['request']
def get_ya_geocode_n_results(): #Выдает, сколько ответов нашел геокодер
  return int(ya_geocode_data['metaDataProperty']['GeocoderResponseMetaData']['found'])
def get_ya_geocode_results(): #Возвращает список адресов и их координат, которые подходят. Пусть пользователь выберет правильный.
  ret = []
  for i in range(get_ya_geocode_n_results()):
    ret.append([ya_geocode_data['featureMember'][i]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text'], ya_geocode_data['featureMember'][i]['GeoObject']['Point']['pos']])
  return ret
def choose_result(n): #n - Номер выбранного ответа. ВОзвращает true если успешно, false - если не подходит
  global choosen_result
  if(n<0 or n >= get_ya_geocode_n_results()):
      return False
  choosen_result = n
  return True
#Работа с выбраным результатом
def get_coords():
    return ya_geocode_data['featureMember'][choosen_result]['GeoObject']['Point']['pos'].split(" ")[::-1]
def ya_id():
  return ya_geocode_data['featureMember'][choosen_result]['GeoObject']['uri']


resolution = 10

def get_cell_id(coords):
    return h3.latlng_to_cell(float(coords[0]), float(coords[1]), resolution)

def get_data_cell(cell_id):
    return data[cell_id]
print("Введите адрес")
addr = input()
ya_geocode(addr)
print("Полученно "+str(get_ya_geocode_n_results())+" результатов")
for i in get_ya_geocode_results():
    print(i)
print("Выберите, с каким результатом вы хотите работать. Введите номер (0, 1 и так далее)")
if(choose_result(int(input()))):
    print("Работаем с координатами:", get_coords())
    print("Это ячейка:", get_cell_id(get_coords()))
    #Информация об этой ячейке хранится в data[cell_id]
else:
    print("Ошибка")


