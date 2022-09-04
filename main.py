import requests
import os
from pprint import pprint
import datetime


class VKDownloader:
    def __init__(self, token):
        self.token = token

    def get_photo(self, offset=0, count=5):
        url = 'https://api.vk.com/method/photos.get'
        params = {'access_token': vktoken, 'v': '5.131', 'owner_id': vk_user_id, 'album_id': 'profile',
                  'extended': '1', 'photo_sizes': '1', 'offset': offset, 'count': count}
        result = requests.get(url, params=params).json()
        # pprint(result)  # почему лезут все фото а не 5? Убрать к дьяволу.
        return result  # {response{count, items[]}}

    def get_all_photo(self):
        if not os.path.exists('vk_photo_backup'):
            os.mkdir('vk_photo_backup')  # создаём папку, если нету
        load = self.get_photo()
        count_all = load['response']['count']
        # print(count_all)
        num = 0  # Отступ
        count = 5  # Кол-во получаемых записей
        photos = []  # Полученные фото
        max_photo = {}  # Фото с максимальным разрешением
        while num <= count_all:
            if num != 0:
                load = self.get_photo(num, count)
            for photo in load['response']['items']: # Ходим по фоткам
                max_size = 0
                # print(photo)
                for size in photo['sizes']:  # Ищем максимальный размер
                    if size['width'] > max_size:
                        max_size = size['width']
                info = {}
                if photo['likes']['count'] not in max_photo.keys():  # Проверяем лайки на совпадения
                    max_photo[photo['likes']['count']] = size['url']
                    info['file_name'] = f'{photo["likes"]["count"]}.jpg'  # И задаём имя либо так, если нету
                else:
                    date = datetime.date.fromordinal(int(photo["date"] / 86400)).strftime('%d.%m.%Y')  # от Unix'a
                    # Дату перекорячить, чтоб год нормально отображался, а не от рождества Юникса
                    max_photo[f'{photo["likes"]["count"]} + {date}'] = size['url']
                    info['file_name'] = f'{photo["likes"]["count"]}_{date}.jpg'  # либо сяк, если есть
                # print(max_size)
                info['size'] = size['type']
                photos.append(info)  # Добавление в список в требуемом виде

            num += count
        #
        # print(photos)
        # print(info)
        # print(max_photo)
        #






if __name__ == '__main__':
    vk_user_id = input('Введите id пользователя ВК: ')
    ya_token = input('Введите токен ЯндексДиск: ')
    with open('vktoken.txt', 'r') as file:
        vktoken = file.readline().strip()
    downloader = VKDownloader(vktoken)
    print(downloader.get_all_photo())

