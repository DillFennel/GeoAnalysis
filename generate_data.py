import geopandas as gpd
import pandas as pd
import numpy as np
import json
import h3
import folium
import osmnx as ox
from shapely import wkt
from folium.plugins import HeatMap
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import contextily as cx
import requests
from statistics import mean

print("Начало работы")
resolution = 10

moscow = ox.geocode_to_gdf('Moscow, Russia')
coords =  json.loads(moscow.to_json())['features'][0]['geometry']['coordinates']
print("Получены координаты Москвы")
lng1 = []
lat1 = []
lng2 = []
lat2 = []
lng3 = []
lat3 = []
for i in coords[0][0]:
    lng1.append(i[0])
    lat1.append(i[1])
for i in coords[1][0]:
    lng2.append(i[0])
    lat2.append(i[1])
for i in coords[2][0]:
    lng3.append(i[0])
    lat3.append(i[1])

poly1 = h3.LatLngPoly([[lat1[i], lng1[i]] for i in range(len(lng1))])
poly2 = h3.LatLngPoly([[lat2[i], lng2[i]] for i in range(len(lng2))])
poly3 = h3.LatLngPoly([[lat3[i], lng3[i]] for i in range(len(lng3))])
big_poly = h3.LatLngMultiPoly(poly1, poly2, poly3)
cells = h3.h3shape_to_cells(big_poly, res=resolution)
print("Ячейки сгенерированны")

mos_data_sets = [
    {'name':'wifi_biblio', 'fullname': 'Wi-Fi в библиотеках', 'mos_id':60788},
    {'name':'wifi_cinema', 'fullname': 'Wi-Fi в кинотеатрах', 'mos_id':60789},
    {'name':'wifi_culture', 'fullname': 'Wi-Fi в культурных центрах', 'mos_id':60790},
    {'name':'wifi_parks', 'fullname': 'Wi-Fi в парках', 'mos_id':861},

    {'name':'bus_stations', 'fullname': 'Автовокзалы и автостанции Москвы', 'mos_id':1881},
    {'name':'racing_tracks_indoor', 'fullname': 'Автодромы спортивные крытые', 'mos_id':1384},
    {'name':'racing_tracks_outdoor', 'fullname': 'Автодромы спортивные открытые', 'mos_id':1385},
    {'name':'gas_stations_not_eco', 'fullname': 'Автозаправочные станции, реализующие топливо, несоответствующее установленным экологическим требованиям', 'mos_id':754},

    {'name':'gas_stations_eco', 'fullname': 'Автозаправочные станции, реализующие топливо, соответствующее установленным экологическим требованиям', 'mos_id':753},
    {'name':'aquaparks', 'fullname': 'Аквапарки', 'mos_id':2269},
    {'name':'attractions_parks', 'fullname': 'Аттракционы в парках и на площадках', 'mos_id':498},
    {'name':'attractions_shopping_centre', 'fullname': 'Аттракционы в торгово-развлекательных комплексах', 'mos_id':3227},
    
    {'name':'airports', 'fullname': 'Аэропорты', 'mos_id':62883},
    {'name':'swimming_pools_indoor', 'fullname': 'Бассейны плавательные крытые', 'mos_id':890},
    {'name':'swimming_pools_outdoor', 'fullname': 'Бассейны плавательные открытые', 'mos_id':894},
    {'name':'botanic_gardens', 'fullname': 'Ботанические сады', 'mos_id':2456},

    {'name':'bicycle_parking', 'fullname': 'Велосипедные парковки', 'mos_id':916},
    {'name':'metro_exits', 'fullname': 'Входы и выходы вестибюлей станций Московского метрополитена', 'mos_id':624},
    {'name':'railway_radial_exits', 'fullname': 'Входы и выходы вестибюлей станций радиальных железнодорожных направлений', 'mos_id':62890},
    {'name':'central_diameter_exits', 'fullname': 'Входы и выходы станций Московских центральных диаметров', 'mos_id':62207},

    {'name':'wifi_city', 'fullname': 'Городской Wi-Fi', 'mos_id':2756},
    {'name':'children_playgrounds', 'fullname': 'Детские игровые площадки в парках', 'mos_id':1389},
    {'name':'children_development_centers', 'fullname': 'Детские развивающие центры', 'mos_id':905},
    {'name':'railway_stations', 'fullname': 'Железнодорожные вокзалы Москвы', 'mos_id':62201},

    {'name':'sports_halls', 'fullname': 'Залы спортивные', 'mos_id':60622},
    {'name':'tennis_halls', 'fullname': 'Залы теннисные', 'mos_id':60623},
    {'name':'gyms', 'fullname': 'Залы тренажерные', 'mos_id':60624},
    {'name':'catholic_churches', 'fullname': 'Католические храмы', 'mos_id':2265},

    {'name':'cinemas', 'fullname': 'Кинотеатры', 'mos_id':495},
    {'name':'ice_fields_indoor', 'fullname': 'Ледовые поля (крытые)', 'mos_id':1232},
    {'name':'transport_stops', 'fullname': 'Маршруты и остановки наземного городского пассажирского транспорта (Остановки)', 'mos_id':60662},
    {'name':'fairs_interregional', 'fullname': 'Межрегиональные ярмарки', 'mos_id':62061},

    {'name':'places_for_activity_with_children', 'fullname': 'Места для досуга и отдыха с детьми', 'mos_id':2249},
    {'name':'places_for_picnic', 'fullname': 'Места для пикника', 'mos_id':912},
    {'name':'places_for_horseriding', 'fullname': 'Места катания на лошадях', 'mos_id':1386},
    {'name':'places_for_collecting_trash', 'fullname': 'Места сбора отходов', 'mos_id':2542},

    {'name':'places_for_collecting_largesize_garbage', 'fullname': 'Места установки бункеров для сбора крупногабаритного мусора', 'mos_id':2470},
    {'name':'mosques', 'fullname': 'Мечети', 'mos_id':2266},
    {'name':'monasteries', 'fullname': 'Монастыри', 'mos_id':2267},
    {'name':'music_venues', 'fullname': 'Музыкальные площадки в парках', 'mos_id':2116},

    {'name':'schools', 'fullname': 'Образовательные учреждения города Москвы', 'mos_id':2263},
    {'name':'public_catering', 'fullname': 'Общественное питание в Москве', 'mos_id':1903},
    {'name':'funeral_service_facilities', 'fullname': 'Объекты ритуального обслуживания', 'mos_id':607},
    {'name':'retail_and_catering_facilities_with_license_for_alcohol', 'fullname': 'Объекты розничной торговли и общественного питания, имеющие лицензию на розничную продажу алкогольной продукции с указанием срока ее действия', 'mos_id':586},
    
    {'name':'universities', 'fullname': 'Организации, осуществляющие образовательную деятельность на территории города Москвы, обучающимся в которых предоставляется право на бесплатное оформление социальной карты студента/ординатора/аспиранта/ассистента-стажера', 'mos_id':3326},
    {'name':'taxi_parking', 'fullname': 'Парковки такси', 'mos_id':621},
    {'name':'park_areas', 'fullname': 'Парковые территории', 'mos_id':1465},
    {'name':'parking_intercepting', 'fullname': 'Перехватывающие парковки', 'mos_id':622},

    {'name':'tourist_information_centers', 'fullname': 'Перечень туристско-информационных центров Москвы', 'mos_id':2465},
    {'name':'paid_parking_closed_type', 'fullname': 'Платные парковки закрытого типа', 'mos_id':1681},
    {'name':'paid_parking_road_network', 'fullname': 'Платные парковки на улично-дорожной сети', 'mos_id':623},
    {'name':'dog_walking_grounds', 'fullname': 'Площадки для выгула (дрессировки) собак', 'mos_id':2663},

    {'name':'regional_fairs', 'fullname': 'Региональные ярмарки', 'mos_id':653},
    {'name':'orthodox_churches', 'fullname': 'Религиозные объекты Русской православной церкви', 'mos_id':2624},
    {'name':'retail_markets', 'fullname': 'Розничные рынки', 'mos_id':654},
    {'name':'synagogues', 'fullname': 'Синагоги', 'mos_id':2268},

    {'name':'stationary_retail_facilities', 'fullname': 'Стационарные торговые объекты', 'mos_id':3304},
    {'name':'weekend Fairs', 'fullname': 'Ярмарки выходного дня', 'mos_id':620}
]

data = {}
for hex in cells:
    data[hex] = {}
    for i in mos_data_sets:
        data[hex][i['name']] = {'n':0}

print("data создана, но пока пуста. Начало заполнения data")
mos_api = ''

for data_set in mos_data_sets:
        id_set = str(data_set['mos_id'])
        #requests.get('https://apidata.mos.ru/v1/datasets/'+id_set+'?api_key='+mos_api).json() Информация по дата-сету
        n = requests.get('https://apidata.mos.ru/v1/datasets/'+id_set+'/count?api_key='+mos_api).json() #Кол-во строк в датасете
        print("Всего строк в дата сете "+data_set['name']+" находится "+str(n)+" строк")
        errors = []
        not_state = []
        skip = 0
        while(n>0):
            if(n>1000):
                data_from_mos = requests.get('https://apidata.mos.ru/v1/features/'+id_set+'?$skip='+str(skip)+'&$top=1000&api_key='+mos_api).json() #Сами строки
                n-=1000
                skip+=1000
            else:
                data_from_mos = requests.get('https://apidata.mos.ru/v1/features/'+id_set+'?$skip='+str(skip)+'&$top='+str(n)+'&api_key='+mos_api).json() #Сами строки
                n=0  
            for i in data_from_mos['features']:
                match id_set:
                    case '495':#Исключение cinemas - координаты хранятся в еще одном массиве
                        cell_id_list = [h3.latlng_to_cell(i['geometry']['coordinates'][0][1], i['geometry']['coordinates'][0][0] , res=resolution)]
                    case '2263':#Исключение schools - Хранят мульти полигоны со всеми корпусами
                        cell_id_list = []
                        for building in i['geometry']['coordinates']:
                            try:
                                cell_id = h3.latlng_to_cell(building[0][0][1], building[0][0][0], resolution)
                            except:
                                cell_id = h3.latlng_to_cell(building[0][1], building[0][0], resolution)
                            cell_id_list.append(cell_id)
                    case '1465':#Исключение park_areas - Хранят полигон
                        cell_id_list = []
                        if(i['geometry']['type'] == 'Polygon'):
                            poly_coords = []
                            for place in i['geometry']['coordinates']:
                                for c in place:
                                    poly_coords.append([c[1], c[0]])
                            poly = h3.LatLngPoly(poly_coords)
                            cells_id_list = h3.h3shape_to_cells(poly, resolution)
                        else:
                            for place in i['geometry']['coordinates']:
                                poly_coords = []
                                for p in place:
                                    for c in p:
                                        poly_coords.append([c[1], c[0]])
                                poly = h3.LatLngPoly(poly_coords)
                                cells_id_list += h3.h3shape_to_cells(poly, resolution)
                    case '1681':#Исключение paid_parking_closed_type - Хранят полигон
                        cell_id_list = [h3.latlng_to_cell(mean([x[1] for x in i['geometry']['coordinates'][0]]), mean([x[0] for x in i['geometry']['coordinates'][0]]), resolution)]
                    case _:
                        try:
                            cell_id_list = [h3.latlng_to_cell(i['geometry']['coordinates'][1], i['geometry']['coordinates'][0] , res=resolution)]
                        except:
                            not_state.append(i)
                for cell_id in cell_id_list:
                    if not(cell_id in data.keys()):
                        errors.append(cell_id)
                    else:
                        data[cell_id][data_set['name']]['n'] += 1
                        try:
                            data[cell_id][data_set['name']]['features'].append(i)
                        except:
                            data[cell_id][data_set['name']]['features'] = [i]
        print("В дата сете "+ data_set['name'] + " было "+str(len(errors))+" немосковских ячеек и "+str(len(not_state))+" пустых координат")
print("data заполнена, записываем в файл")
with open('data.json', 'w') as f:
    json.dump(data, f)
print("Готово")
