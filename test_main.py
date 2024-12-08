import unittest  # Модуль для написания юнит-тестов
import json  # Модуль для работы с JSON-данными
import requests  # Модуль для выполнения HTTP-запросов
import h3  # Модуль для работы с геопространственными данными

# API-ключ для Яндекс Геокодера
ya_geocode_api = 'cb66d83b-7594-40d2-859a-86cbcdb0d20d'
# Разрешение для H3-индекса
resolution = 10

# Список наборов данных, доступных для анализа
mos_data_sets = [
    {'name': 'wifi_biblio', 'fullname': 'Wi-Fi в библиотеках', 'mos_id': 60788},
    {'name': 'wifi_cinema', 'fullname': 'Wi-Fi в кинотеатрах', 'mos_id': 60789},
    {'name': 'wifi_culture', 'fullname': 'Wi-Fi в культурных центрах', 'mos_id': 60790},
    {'name': 'wifi_parks', 'fullname': 'Wi-Fi в парках', 'mos_id': 861},

    {'name': 'bus_stations', 'fullname': 'Автовокзалы и автостанции Москвы', 'mos_id': 1881},
    {'name': 'racing_tracks_indoor', 'fullname': 'Автодромы спортивные крытые', 'mos_id': 1384},
    {'name': 'racing_tracks_outdoor', 'fullname': 'Автодромы спортивные открытые', 'mos_id': 1385},
    {'name': 'gas_stations_not_eco',
     'fullname': 'Автозаправочные станции, реализующие топливо, несоответствующее установленным экологическим требованиям',
     'mos_id': 754},

    {'name': 'gas_stations_eco',
     'fullname': 'Автозаправочные станции, реализующие топливо, соответствующее установленным экологическим требованиям',
     'mos_id': 753},
    {'name': 'aquaparks', 'fullname': 'Аквапарки', 'mos_id': 2269},
    {'name': 'attractions_parks', 'fullname': 'Аттракционы в парках и на площадках', 'mos_id': 498},
    {'name': 'attractions_shopping_centre', 'fullname': 'Аттракционы в торгово-развлекательных комплексах',
     'mos_id': 3227},

    {'name': 'airports', 'fullname': 'Аэропорты', 'mos_id': 62883},
    {'name': 'swimming_pools_indoor', 'fullname': 'Бассейны плавательные крытые', 'mos_id': 890},
    {'name': 'swimming_pools_outdoor', 'fullname': 'Бассейны плавательные открытые', 'mos_id': 894},
    {'name': 'botanic_gardens', 'fullname': 'Ботанические сады', 'mos_id': 2456},

    {'name': 'bicycle_parking', 'fullname': 'Велосипедные парковки', 'mos_id': 916},
    {'name': 'metro_exits', 'fullname': 'Входы и выходы вестибюлей станций Московского метрополитена', 'mos_id': 624},
    {'name': 'railway_radial_exits',
     'fullname': 'Входы и выходы вестибюлей станций радиальных железнодорожных направлений', 'mos_id': 62890},
    {'name': 'central_diameter_exits', 'fullname': 'Входы и выходы станций Московских центральных диаметров',
     'mos_id': 62207},

    {'name': 'wifi_city', 'fullname': 'Городской Wi-Fi', 'mos_id': 2756},
    {'name': 'children_playgrounds', 'fullname': 'Детские игровые площадки в парках', 'mos_id': 1389},
    {'name': 'children_development_centers', 'fullname': 'Детские развивающие центры', 'mos_id': 905},
    {'name': 'railway_stations', 'fullname': 'Железнодорожные вокзалы Москвы', 'mos_id': 62201},

    {'name': 'sports_halls', 'fullname': 'Залы спортивные', 'mos_id': 60622},
    {'name': 'tennis_halls', 'fullname': 'Залы теннисные', 'mos_id': 60623},
    {'name': 'gyms', 'fullname': 'Залы тренажерные', 'mos_id': 60624},
    {'name': 'catholic_churches', 'fullname': 'Католические храмы', 'mos_id': 2265},

    {'name': 'cinemas', 'fullname': 'Кинотеатры', 'mos_id': 495},
    {'name': 'ice_fields_indoor', 'fullname': 'Ледовые поля (крытые)', 'mos_id': 1232},
    {'name': 'transport_stops',
     'fullname': 'Маршруты и остановки наземного городского пассажирского транспорта (Остановки)', 'mos_id': 60662},
    {'name': 'fairs_interregional', 'fullname': 'Межрегиональные ярмарки', 'mos_id': 62061},

    {'name': 'places_for_activity_with_children', 'fullname': 'Места для досуга и отдыха с детьми', 'mos_id': 2249},
    {'name': 'places_for_picnic', 'fullname': 'Места для пикника', 'mos_id': 912},
    {'name': 'places_for_horseriding', 'fullname': 'Места катания на лошадях', 'mos_id': 1386},
    {'name': 'places_for_collecting_trash', 'fullname': 'Места сбора отходов', 'mos_id': 2542},

    {'name': 'places_for_collecting_largesize_garbage',
     'fullname': 'Места установки бункеров для сбора крупногабаритного мусора', 'mos_id': 2470},
    {'name': 'mosques', 'fullname': 'Мечети', 'mos_id': 2266},
    {'name': 'monasteries', 'fullname': 'Монастыри', 'mos_id': 2267},
    {'name': 'music_venues', 'fullname': 'Музыкальные площадки в парках', 'mos_id': 2116},

    {'name': 'schools', 'fullname': 'Образовательные учреждения города Москвы', 'mos_id': 2263},
    {'name': 'public_catering', 'fullname': 'Общественное питание в Москве', 'mos_id': 1903},
    {'name': 'funeral_service_facilities', 'fullname': 'Объекты ритуального обслуживания', 'mos_id': 607},
    {'name': 'retail_and_catering_facilities_with_license_for_alcohol',
     'fullname': 'Объекты розничной торговли и общественного питания, имеющие лицензию на розничную продажу алкогольной продукции с указанием срока ее действия',
     'mos_id': 586},

    {'name': 'universities',
     'fullname': 'Организации, осуществляющие образовательную деятельность на территории города Москвы, обучающимся в которых предоставляется право на бесплатное оформление социальной карты студента/ординатора/аспиранта/ассистента-стажера',
     'mos_id': 3326},
    {'name': 'taxi_parking', 'fullname': 'Парковки такси', 'mos_id': 621},
    {'name': 'park_areas', 'fullname': 'Парковые территории', 'mos_id': 1465},
    {'name': 'parking_intercepting', 'fullname': 'Перехватывающие парковки', 'mos_id': 622},

    {'name': 'tourist_information_centers', 'fullname': 'Перечень туристско-информационных центров Москвы',
     'mos_id': 2465},
    {'name': 'paid_parking_closed_type', 'fullname': 'Платные парковки закрытого типа', 'mos_id': 1681},
    {'name': 'paid_parking_road_network', 'fullname': 'Платные парковки на улично-дорожной сети', 'mos_id': 623},
    {'name': 'dog_walking_grounds', 'fullname': 'Площадки для выгула (дрессировки) собак', 'mos_id': 2663},

    {'name': 'regional_fairs', 'fullname': 'Региональные ярмарки', 'mos_id': 653},
    {'name': 'orthodox_churches', 'fullname': 'Религиозные объекты Русской православной церкви', 'mos_id': 2624},
    {'name': 'retail_markets', 'fullname': 'Розничные рынки', 'mos_id': 654},
    {'name': 'synagogues', 'fullname': 'Синагоги', 'mos_id': 2268},

    {'name': 'stationary_retail_facilities', 'fullname': 'Стационарные торговые объекты', 'mos_id': 3304},
    {'name': 'weekend_fairs', 'fullname': 'Ярмарки выходного дня', 'mos_id': 620}
]

class TestGeoAnalysis(unittest.TestCase):
    """
    Класс для тестирования геопространственного анализа.
    """

    def test_geo_analysis(self):
        """
        Тестовый метод для проверки геопространственного анализа.
        """
        # Список адресов для тестирования
        addresses = [
            "Ивановская площадь",
            "Февральская 19А",
            "Береговой пр., 5, корп. 1, Москва",
            "Ленинский проспект, 32",
            "Большая Дмитровка, 7с1",
            "Тверская улица, 4",
            "Новый Арбат, 32",
            "Кузнецкий Мост, 6/3",
            "Никольская улица, 10",
            "Пушкинская площадь, 2",
            "Манежная площадь, 1"
        ]

        for address in addresses:
            # Выполнение запроса к Яндекс Геокодеру для получения координат адреса
            response = requests.get(
                f'https://geocode-maps.yandex.ru/1.x/?apikey={ya_geocode_api}&geocode={address.replace(" ", "+")}&format=json'
            )
            # Проверка, что статус ответа равен 200 (успешный запрос)
            self.assertEqual(response.status_code, 200, f"Ошибка при запросе к API для адреса: {address}")

            # Получение списка найденных объектов для данного адреса
            features = response.json()['response']['GeoObjectCollection']['featureMember']
            # Проверка, что найден хотя бы один объект для данного адреса
            self.assertGreater(len(features), 0, f"Нет данных для адреса: {address}")

            # Получение координат первого найденного объекта
            coords = features[0]['GeoObject']['Point']['pos'].split(" ")[::-1]
            # Вычисление H3-индекса для полученных координат
            hex_id = h3.latlng_to_cell(float(coords[0]), float(coords[1]), resolution)

            # Получение списков ячеек H3-индекса для внутреннего и внешнего кольца
            cells_inner = h3.grid_ring(hex_id, 1)
            cells_inner.append(hex_id)
            cells_outer = h3.grid_ring(hex_id, 2)

            # Проверка наличия данных для каждого набора данных
            no_data_sets = []
            for data_set in mos_data_sets:
                with open(f"data/{data_set['name']}.json", 'r') as file:
                    data_from_json = json.load(file)

                    # Проверка, что хотя бы одна ячейка из внутреннего или внешнего кольца
                    # присутствует в данных для текущего набора
                    found_inner = any(cell in data_from_json.keys() for cell in cells_inner)
                    found_outer = any(cell in data_from_json.keys() for cell in cells_outer)

                    # Если данные не найдены, добавляем название набора в список no_data_sets
                    if not found_inner or not found_outer:
                        no_data_sets.append(data_set['fullname'])

            # Вывод информации о наличии/отсутствии данных для каждого адреса
            if no_data_sets:
                print(f"Нет данных для адреса {address} в следующих наборах данных: {', '.join(no_data_sets)}")
            else:
                print("Данные найдены для всех наборов.")

if __name__ == '__main__':
    # Запуск юнит-тестов
    unittest.main()
