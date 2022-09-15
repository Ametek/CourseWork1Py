import requests
import os
import time
import json
from tqdm import tqdm


class VKDownloader:
    def __init__(self, vktoken):
        self.vktoken = vktoken

    def get_photo(self, count=5, vk_user_id=None):
        url = 'https://api.vk.com/method/photos.get'
        params = {'access_token': self.vktoken, 'v': '5.131', 'owner_id': vk_user_id, 'album_id': 'profile',
                  'extended': '1', 'photo_sizes': '1', 'count': count}
        response = requests.get(url, params=params).json()
        return response

    def get_all_photo(self, vk_user_id):
        if not os.path.exists('vk_photo_backup'):
            os.mkdir('vk_photo_backup')  # создаём папку, если нету
        count = 5  # Кол-во получаемых записей
        load = self.get_photo(count, vk_user_id)
        photos = []  # Полученные фото
        max_photo = {}  # Фото с максимальным разрешением

        print('Обработка данных:')
        for photo in tqdm(load['response']['items'], ncols=93, unit_scale=True): # Ходим по фоткам
            max_size = 0
            for size in photo['sizes']:  # Ищем максимальный размер
                if size['width'] > max_size:
                    max_size = size['width']
            info = {}
            if photo['likes']['count'] not in max_photo.keys():  # Проверяем лайки на совпадения
                max_photo[photo['likes']['count']] = size['url']
                info['file_name'] = f'{photo["likes"]["count"]}.jpg'  # И задаём имя либо так, если нету
            else:
                date = time.strftime('%d.%m.%Y', time.localtime(photo['date']))
                max_photo[f'{photo["likes"]["count"]}_{date}'] = size['url']
                info['file_name'] = f'{photo["likes"]["count"]}_{date}.jpg'  # либо сяк, если есть
            info['size'] = size['type']
            photos.append(info)  # Добавление в список в требуемом виде

        with open('vk_photo_backup.json', 'w') as file:
            json.dump(photos, file, indent=4, sort_keys=False)

        time.sleep(0.1)
        print('Скачивание фото:')
        for name, url in tqdm(max_photo.items(), ncols=100, unit_scale=True):
            with open(f'vk_photo_backup/{name}.jpg', 'wb') as file:
                image = requests.get(url)
                file.write(image.content)  # Сохраняем фото в папку
        return
